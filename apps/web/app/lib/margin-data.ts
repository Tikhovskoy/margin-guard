export type MarginStatus = "healthy" | "attention" | "critical" | "incomplete";

export type MarginRow = {
  sku: string;
  product: string;
  revenue: number;
  fees: number;
  cost: number | null;
  margin: number | null;
  percent: number | null;
  status: MarginStatus;
};

export type MarginPreviewItem = {
  sku: string;
  revenue: string;
  marketplace_fees: string;
  cost_price: string | null;
  margin: string | null;
  margin_percent: string | null;
  calculation_status: "complete" | "missing_cost";
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

export type PortfolioMetrics = {
  completeCount: number;
  incompleteCount: number;
  totalRevenue: number;
  totalFees: number;
  totalCost: number;
  totalMargin: number;
  weightedMarginPercent: number;
};

export function getMarginStatus(percent: number | null): MarginStatus {
  if (percent === null) return "incomplete";
  if (percent < 20) return "critical";
  if (percent < 25) return "attention";
  return "healthy";
}

export function mapMarginPreviewItems(items: MarginPreviewItem[]): MarginRow[] {
  return items.map((item) => {
    const percent = item.margin_percent === null ? null : Number(item.margin_percent);
    return {
      sku: item.sku,
      product: productNames[item.sku] ?? `Товар ${item.sku}`,
      revenue: Number(item.revenue),
      fees: Number(item.marketplace_fees),
      cost: item.cost_price === null ? null : Number(item.cost_price),
      margin: item.margin === null ? null : Number(item.margin),
      percent,
      status: getMarginStatus(percent),
    };
  });
}

export function calculatePortfolioMetrics(rows: MarginRow[]): PortfolioMetrics {
  const completeRows = rows.filter(
    (row) => row.cost !== null && row.margin !== null && row.percent !== null,
  );
  const totalRevenue = completeRows.reduce((total, row) => total + row.revenue, 0);
  const totalFees = completeRows.reduce((total, row) => total + row.fees, 0);
  const totalCost = completeRows.reduce((total, row) => total + (row.cost ?? 0), 0);
  const totalMargin = completeRows.reduce((total, row) => total + (row.margin ?? 0), 0);

  return {
    completeCount: completeRows.length,
    incompleteCount: rows.length - completeRows.length,
    totalRevenue,
    totalFees,
    totalCost,
    totalMargin,
    weightedMarginPercent: totalRevenue > 0 ? totalMargin / totalRevenue * 100 : 0,
  };
}
