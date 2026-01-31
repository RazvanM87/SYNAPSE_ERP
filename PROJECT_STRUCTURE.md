# 📘 SYNAPSE ERP – Documentație structură proiect

## Core
- **core/**
  - **core\auth/**
      - auth_controller.py
      - auth_service.py
  - **core\config/**
      - settings_service.py

## Operational
- **operational/**
  - **operational\clients/**
      - client_controller.py
      - client_service.py
  - **operational\invoices/**
      - invoice_controller.py
      - invoice_service.py

## Ai
- **ai/**
  - **ai\predictions/**
      - sales_model.py

## Bi
- **bi/**
  - **bi\dashboard/**
      - finance_dashboard.py

## Tests
- **tests/**
  - **tests\ai/**
      - test_sales_predictions.py
  - **tests\bi/**
      - test_finance_dashboard.py
  - **tests\core/**
      - test_auth.py
  - **tests\operational/**
      - test_clients.py
      - test_invoices.py

