Workers folder: implement Celery / RQ workers here.
- process_acta: download image from storage, run OCR, extract counts, call service.process_acta
- retry and DLQ: implement retry policies and dead-letter queue for failed actas
