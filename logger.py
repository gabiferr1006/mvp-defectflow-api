import logging

# Configuração simples de log para uso em desenvolvimento acadêmico.
# Os logs serão exibidos no terminal, sem gravação em arquivo,
# evitando bloqueios de arquivo no Windows durante o desenvolvimento.

logger = logging.getLogger("defectflow-api")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)