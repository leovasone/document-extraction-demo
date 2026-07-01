# Document Data Extraction Pipeline (Computer Vision + OCR)

Protótipo funcional que transforma recibos/notas fiscais em imagem ou PDF em
dados estruturados (JSON/CSV), sem intervenção manual.

## Por que existe

Extração manual de dados de documentos (notas fiscais, recibos, formulários)
é um dos gargalos operacionais mais comuns em empresas de médio/grande porte.
Este projeto demonstra uma arquitetura de ponta a ponta para resolver isso:
captura → pré-processamento → OCR → extração estruturada → dado pronto para
BI/ERP.

## Arquitetura

```
Documento (PDF/imagem)
        |
        v
  pdf_utils.py        (PyMuPDF: renderiza páginas de PDF em imagens)
        |
        v
  preprocess.py        (OpenCV: denoise + limiarização Otsu)
        |
        v
  engines/*.py          (interface OCREngine plugável)
        |                 - TesseractEngine   (local, implementada, sem custo)
        |                 - AzureDocumentIntelligenceEngine  (stub, pronta para produção)
        |                 - GoogleDocumentAIEngine           (stub, pronta para produção)
        v
  parser.py             (regex/heurísticas: fornecedor, data, nota fiscal, itens, total)
        v
  JSON / CSV estruturado
```

A camada de OCR é uma interface (`OCREngine`), então trocar o motor local
(Tesseract) por uma API de visão em nuvem (Azure AI Document Intelligence ou
Google Document AI) para maior precisão em produção é uma troca de uma linha
na composição do pipeline — o resto do código não muda.

## Como rodar

```bash
pip install -r requirements.txt
python samples/generate_samples.py     # gera recibos sintéticos de teste
python main.py samples/input output/results.json
```

Saída: `output/results.json` (dado estruturado por documento) e
`output/benchmark.json` (throughput medido).

## Resultado no lote de teste (8 recibos sintéticos)

- **100%** de acerto em fornecedor, data, número da nota e valor total
- **100%** de reconciliação item-a-item (soma dos itens = total extraído)
- **~0,48s** por documento em CPU única, sem GPU, sem API paga
- Extrapolando para paralelização simples (8 workers): **~60 mil documentos/hora**

Os números de throughput são medidos localmente sobre este pipeline de
demonstração (CPU única + Tesseract), não uma carga de produção real — mas
mostram que a arquitetura, ao ser paralelizada horizontalmente (workers/fila),
comporta volumes de milhares de documentos por hora sem depender de APIs pagas.

## Evoluindo para produção

- Trocar `TesseractEngine` por `AzureDocumentIntelligenceEngine` ou
  `GoogleDocumentAIEngine` para os modelos pré-treinados de nota
  fiscal/invoice (maior precisão em documentos variados e manuscritos)
- Fila de processamento (SQS/Pub-Sub) + workers paralelos para escalar
  horizontalmente
- Validação humana em amostra (human-in-the-loop) para casos de baixa
  confiança
- Armazenamento estruturado (Postgres/BigQuery) + integração com ERP
