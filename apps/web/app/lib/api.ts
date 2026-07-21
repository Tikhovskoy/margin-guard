export type MarginPreview = {
  marketplace: string;
  items: Array<{
    sku: string;
    revenue: string;
    marketplace_fees: string;
    cost_price: string;
    margin: string;
    margin_percent: string;
  }>;
  alerts: Array<{ sku: string; margin_percent: string; threshold_percent: string; message: string }>;
};

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function getMarginPreview(): Promise<MarginPreview> {
  const response = await fetch(`${apiUrl}/api/v1/margins/preview`);
  if (!response.ok) {
    throw new Error("Не удалось загрузить preview маржи.");
  }
  return response.json() as Promise<MarginPreview>;
}
