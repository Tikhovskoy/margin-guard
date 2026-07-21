# margin-guard web

Модуль frontend для dashboard контроля маржи.

## Структура

- `app/components` — UI-компоненты dashboard;
- `app/lib` — типы, mock-данные и клиент API;
- `app/page.tsx` — композиция главной страницы.

## Локальный запуск

```bash
npm ci
npm run dev
```

По умолчанию API ожидается на `http://localhost:8000`. Для другого адреса
создайте `.env.local` на основе `.env.example`.
