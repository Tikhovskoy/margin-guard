export type MarginStatus = "healthy" | "attention" | "critical" | "incomplete";

export type MarginRow = {
  sku: string;
  sourceOperationId: string;
  quantity: number;
  product: string;
  revenue: number;
  fees: number;
  unitCost: number | null;
  cost: number | null;
  margin: number | null;
  percent: number | null;
  status: MarginStatus;
  rrdId: string | null;
  srid: string | null;
  reportId: string | null;
};

export type MarginPreviewItem = {
  sku: string;
  source_operation_id: string;
  quantity: number;
  revenue: string;
  marketplace_fees: string;
  cost_price: string | null;
  cost_amount: string | null;
  margin: string | null;
  margin_percent: string | null;
  rrd_id: string | null;
  srid: string | null;
  report_id: string | null;
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
  { sku: "WB-001", sourceOperationId: "demo-wb-001", quantity: 1, product: "Термокружка 450 мл", revenue: 1500, fees: 345, unitCost: 600, cost: 600, margin: 555, percent: 37, status: "healthy", rrdId: null, srid: null, reportId: null },
  { sku: "WB-002", sourceOperationId: "demo-wb-002", quantity: 1, product: "Органайзер для кухни", revenue: 800, fees: 440, unitCost: 250, cost: 250, margin: 110, percent: 13.75, status: "critical", rrdId: null, srid: null, reportId: null },
  { sku: "WB-014", sourceOperationId: "demo-wb-014", quantity: 1, product: "Набор контейнеров", revenue: 2250, fees: 517, unitCost: 940, cost: 940, margin: 793, percent: 35.24, status: "healthy", rrdId: null, srid: null, reportId: null },
  { sku: "WB-021", sourceOperationId: "demo-wb-021", quantity: 1, product: "Бутылка спортивная", revenue: 1240, fees: 310, unitCost: 510, cost: 510, margin: 420, percent: 33.87, status: "healthy", rrdId: null, srid: null, reportId: null },
  { sku: "WB-033", sourceOperationId: "demo-wb-033", quantity: 1, product: "Щётка для одежды", revenue: 690, fees: 207, unitCost: 335, cost: 335, margin: 148, percent: 21.45, status: "attention", rrdId: null, srid: null, reportId: null },
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
      sourceOperationId: item.source_operation_id,
      quantity: item.quantity,
      product: productNames[item.sku] ?? `Товар ${item.sku}`,
      revenue: Number(item.revenue),
      fees: Number(item.marketplace_fees),
      unitCost: item.cost_price === null ? null : Number(item.cost_price),
      cost: item.cost_amount === null ? null : Number(item.cost_amount),
      margin: item.margin === null ? null : Number(item.margin),
      percent,
      status: getMarginStatus(percent),
      rrdId: item.rrd_id,
      srid: item.srid,
      reportId: item.report_id,
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
