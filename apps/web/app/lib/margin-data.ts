export type MarginStatus = "healthy" | "attention" | "critical";

export type MarginRow = {
  sku: string;
  product: string;
  revenue: number;
  fees: number;
  cost: number;
  margin: number;
  percent: number;
  status: MarginStatus;
};

export const productNames: Record<string, string> = {
  "WB-001": "Термокружка 450 мл",
  "WB-002": "Органайзер для кухни",
  "WB-014": "Набор контейнеров",
  "WB-021": "Бутылка спортивная",
  "WB-033": "Щётка для одежды",
};

export const demoMarginRows: MarginRow[] = [
  { sku: "WB-001", product: "Термокружка 450 мл", revenue: 1500, fees: 345, cost: 600, margin: 555, percent: 37, status: "healthy" },
  { sku: "WB-002", product: "Органайзер для кухни", revenue: 800, fees: 440, cost: 250, margin: 110, percent: 13.75, status: "critical" },
  { sku: "WB-014", product: "Набор контейнеров", revenue: 2250, fees: 517, cost: 940, margin: 793, percent: 35.24, status: "healthy" },
  { sku: "WB-021", product: "Бутылка спортивная", revenue: 1240, fees: 310, cost: 510, margin: 420, percent: 33.87, status: "healthy" },
  { sku: "WB-033", product: "Щётка для одежды", revenue: 690, fees: 207, cost: 335, margin: 148, percent: 21.45, status: "attention" },
];

export const formatCurrency = (value: number) =>
  new Intl.NumberFormat("ru-RU", {
    style: "currency",
    currency: "RUB",
    maximumFractionDigits: 0,
  }).format(value);

export function getMarginStatus(percent: number): MarginStatus {
  if (percent < 20) return "critical";
  if (percent < 25) return "attention";
  return "healthy";
}
