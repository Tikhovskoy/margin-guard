import { describe, expect, it } from "vitest";

import {
  calculatePortfolioMetrics,
  getMarginStatus,
  mapMarginPreviewItems,
  type MarginRow,
} from "./margin-data";

describe("getMarginStatus", () => {
  it.each([
    [19.99, "critical"],
    [20, "attention"],
    [24.99, "attention"],
    [25, "healthy"],
  ] as const)("assigns %s%% to %s", (percent, expected) => {
    expect(getMarginStatus(percent)).toBe(expected);
  });

  it("marks a position without a calculation as incomplete", () => {
    expect(getMarginStatus(null)).toBe("incomplete");
  });
});

describe("mapMarginPreviewItems", () => {
  it("maps API decimals and known product names to dashboard rows", () => {
    const [row] = mapMarginPreviewItems([{
      sku: "WB-001",
      source_operation_id: "mock-wb-001",
      quantity: 2,
      revenue: "3000.00",
      marketplace_fees: "690.00",
      cost_price: "600.00",
      cost_amount: "1200.00",
      margin: "1110.00",
      margin_percent: "37.00",
      rrd_id: "100001",
      srid: "mock-srid-001",
      report_id: "5001",
      calculation_status: "complete",
    }]);

    expect(row).toEqual({
      sku: "WB-001",
      sourceOperationId: "mock-wb-001",
      quantity: 2,
      product: "Термокружка 450 мл",
      revenue: 3000,
      fees: 690,
      unitCost: 600,
      cost: 1200,
      margin: 1110,
      percent: 37,
      status: "healthy",
      rrdId: "100001",
      srid: "mock-srid-001",
      reportId: "5001",
    });
  });

  it("uses a readable fallback for an unknown SKU", () => {
    const [row] = mapMarginPreviewItems([{
      sku: "WB-900",
      source_operation_id: "mock-wb-900",
      quantity: 1,
      revenue: "100",
      marketplace_fees: "20",
      cost_price: "60",
      cost_amount: "60",
      margin: "20",
      margin_percent: "20",
      rrd_id: null,
      srid: null,
      report_id: null,
      calculation_status: "complete",
    }]);

    expect(row.product).toBe("Товар WB-900");
    expect(row.status).toBe("attention");
  });


  it("keeps missing cost as an incomplete row", () => {
    const [row] = mapMarginPreviewItems([{
      sku: "WB-404",
      source_operation_id: "mock-wb-404",
      quantity: 1,
      revenue: "1000",
      marketplace_fees: "200",
      cost_price: null,
      cost_amount: null,
      margin: null,
      margin_percent: null,
      rrd_id: null,
      srid: null,
      report_id: null,
      calculation_status: "missing_cost",
    }]);

    expect(row.cost).toBeNull();
    expect(row.margin).toBeNull();
    expect(row.percent).toBeNull();
    expect(row.status).toBe("incomplete");
  });
});

describe("calculatePortfolioMetrics", () => {
  it("calculates a revenue-weighted margin and excludes incomplete rows", () => {
    const rows: MarginRow[] = [
      { sku: "A", sourceOperationId: "A-1", quantity: 1, product: "A", revenue: 100, fees: 20, unitCost: 70, cost: 70, margin: 10, percent: 10, status: "critical", rrdId: null, srid: null, reportId: null },
      { sku: "B", sourceOperationId: "B-1", quantity: 1, product: "B", revenue: 900, fees: 90, unitCost: 360, cost: 360, margin: 450, percent: 50, status: "healthy", rrdId: null, srid: null, reportId: null },
      { sku: "C", sourceOperationId: "C-1", quantity: 1, product: "C", revenue: 500, fees: 50, unitCost: null, cost: null, margin: null, percent: null, status: "incomplete", rrdId: null, srid: null, reportId: null },
    ];

    expect(calculatePortfolioMetrics(rows)).toEqual({
      completeCount: 2,
      incompleteCount: 1,
      totalRevenue: 1000,
      totalFees: 110,
      totalCost: 430,
      totalMargin: 460,
      weightedMarginPercent: 46,
    });
  });
});
