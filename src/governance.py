import csv
import getpass
import hashlib
import json
import os
import uuid
from datetime import datetime, timezone

from cryptography.fernet import Fernet

# Sentinel hash used as prev_hash for the very first data row
_GENESIS_HASH = "0" * 64

_HEADER = [
    "row_id",
    "timestamp",
    "user_id",
    "query",
    "sources",
    "response",
    "prev_hash",
    "row_hash",
]


class GovernanceLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self.log_path = os.path.join(log_dir, "audit_log.csv")
        self._key_path = os.path.join(log_dir, ".vault_key")

        os.makedirs(log_dir, exist_ok=True)
        self._fernet = Fernet(self._load_or_create_key())

        if not os.path.exists(self.log_path):
            self._write_header()

    # ------------------------------------------------------------------
    # Key management
    # ------------------------------------------------------------------

    def _load_or_create_key(self) -> bytes:
        if os.path.exists(self._key_path):
            with open(self._key_path, "rb") as f:
                return f.read().strip()

        key = Fernet.generate_key()
        with open(self._key_path, "wb") as f:
            f.write(key)
        # Restrict permissions on POSIX systems
        try:
            os.chmod(self._key_path, 0o600)
        except AttributeError:
            pass  # Windows — skip chmod
        return key

    # ------------------------------------------------------------------
    # CSV helpers
    # ------------------------------------------------------------------

    def _write_header(self) -> None:
        with open(self.log_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(_HEADER)

    def _get_last_hash(self) -> str:
        """Return the row_hash of the last data row, or the genesis sentinel."""
        if not os.path.exists(self.log_path):
            return _GENESIS_HASH

        last_hash = _GENESIS_HASH
        with open(self.log_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("row_hash"):
                    last_hash = row["row_hash"]
        return last_hash

    # ------------------------------------------------------------------
    # Hashing
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_row_hash(row_fields: list[str], prev_hash: str) -> str:
        """SHA-256 of all field values concatenated with prev_hash."""
        payload = "|".join(row_fields) + prev_hash
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    # ------------------------------------------------------------------
    # Encryption helpers
    # ------------------------------------------------------------------

    def _encrypt(self, value: str) -> str:
        return self._fernet.encrypt(value.encode("utf-8")).decode("utf-8")

    def decrypt(self, ciphertext: str) -> str:
        """Decrypt a previously encrypted field value."""
        return self._fernet.decrypt(ciphertext.encode("utf-8")).decode("utf-8")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def log_query(
        self,
        query: str,
        sources: list[dict],
        response: str,
        user_id: str | None = None,
    ) -> None:
        """Append one encrypted, hash-chained audit row to the CSV."""
        row_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        user_id = user_id or getpass.getuser()
        enc_query = self._encrypt(query)
        sources_json = json.dumps(sources, ensure_ascii=False)
        enc_response = self._encrypt(response)

        prev_hash = self._get_last_hash()

        row_fields = [row_id, timestamp, user_id, enc_query, sources_json, enc_response, prev_hash]
        row_hash = self._compute_row_hash(row_fields, prev_hash)

        with open(self.log_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([*row_fields, row_hash])

    # ------------------------------------------------------------------
    # Tamper verification (offline utility)
    # ------------------------------------------------------------------

    def verify_integrity(self) -> tuple[bool, list[str]]:
        """
        Re-compute the hash chain and return (all_valid, list_of_violations).
        A violation message is appended for every row whose stored hash
        does not match the recomputed hash.
        """
        violations: list[str] = []
        prev_hash = _GENESIS_HASH

        with open(self.log_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                stored_hash = row.get("row_hash", "")
                row_fields = [
                    row["row_id"],
                    row["timestamp"],
                    row["user_id"],
                    row["query"],
                    row["sources"],
                    row["response"],
                    row["prev_hash"],
                ]
                expected_hash = self._compute_row_hash(row_fields, row["prev_hash"])
                if expected_hash != stored_hash:
                    violations.append(
                        f"Row {row['row_id']} ({row['timestamp']}): hash mismatch"
                    )
                prev_hash = stored_hash

        return (len(violations) == 0, violations)
