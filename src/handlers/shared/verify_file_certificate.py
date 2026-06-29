import re
import subprocess


class VerifyFileCertificate:
    @staticmethod
    def verify(file_path, signer_subject=None, signer_issuer=None,
               timestamp_subject=None, timestamp_issuer=None,
               signature_type=None, enable_crl_check=False):
        """
        USAGE EXAMPLE:
        verify("C:\\path\\to\\file.exe", signer_subject="CN=Example Signer, O=Example Org, C=US")
        ARGS:
            file_path: Path to the File to Verify
            signer_subject: Expected Signer Subject (Optional)
            signer_issuer: Expected Signer Issuer (Optional)
            timestamp_subject: Expected Timestamp Signer Subject (Optional)
            timestamp_issuer: Expected Timestamp Signer Issuer (Optional)
            signature_type: Expected Signature Type, e.g. Authenticode (Optional)
            enable_crl_check: Whether to Enable Certificate Revocation List Check (Optional)
        """
        cmd = f'Get-AuthenticodeSignature -FilePath "{file_path}"'
        if enable_crl_check:
            cmd += " -Verbose"
        cmd += " | Format-List *"

        try:
            result = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", cmd],
                capture_output=True, text=True, shell=False,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except Exception:
            return False

        output = result.stdout
        if not output:
            return False

        props = {}
        lines = output.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            match = re.match(r"^(\w[\w.]*)\s+:\s*(.*)", line)
            if match:
                key = match.group(1)
                value = match.group(2)
                # Handle multi-line values.
                while i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if next_line and (next_line[0] in (" ", "\t")):
                        value += "\n" + next_line
                        i += 1
                    else:
                        break
                props[key] = value.strip()
            i += 1

        # Return False if status is not Valid.
        if props.get("Status") != "Valid":
            return False

        # Check SignatureType if provided.
        if signature_type is not None and props.get("SignatureType") != signature_type:
            return False

        # Check SignerCertificate Subject and Issuer if provided.
        signer_block = props.get("SignerCertificate", "")
        signer_subject_value = VerifyFileCertificate._parse_cert_field(signer_block, "Subject")
        signer_issuer_value = VerifyFileCertificate._parse_cert_field(signer_block, "Issuer")

        if signer_subject is not None and signer_subject_value != signer_subject:
            return False
        if signer_issuer is not None and signer_issuer_value != signer_issuer:
            return False

        # Check TimeStamperCertificate Subject and Issuer if provided.
        if timestamp_subject is not None or timestamp_issuer is not None:
            stamper_block = props.get("TimeStamperCertificate", "")
            if not stamper_block:
                return False
            stamper_subject_value = VerifyFileCertificate._parse_cert_field(stamper_block, "Subject")
            stamper_issuer_value = VerifyFileCertificate._parse_cert_field(stamper_block, "Issuer")
            if timestamp_subject is not None and stamper_subject_value != timestamp_subject:
                return False
            if timestamp_issuer is not None and stamper_issuer_value != timestamp_issuer:
                return False

        return True

    @staticmethod
    def _parse_cert_field(block, field_name):
        # Use regex to find the field in the block and return its value.
        pattern = re.compile(
            fr"\[{re.escape(field_name)}]\s*\n(.+?)(?=\n\s*\[|\Z)",
            re.DOTALL
        )
        match = pattern.search(block)
        if match:
            return match.group(1).strip()
        return None
