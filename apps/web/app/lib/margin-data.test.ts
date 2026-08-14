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
      revenue: "1500.00",
      marketplace_fees: "345.00",
      cost_price: "600.00",
      margin: "555.00",
      margin_percent: "37.00",
      calculation_status: "complete",
    }]);

    expect(row).toEqual({
      sku: "WB-001",
      product: "Термокружка 450 мл",
      revenue: 1500,
      fees: 345,
      cost: 600,
      margin: 555,
      percent: 37,
      status: "healthy",
    });
  });

  it("uses a readable fallback for an unknown SKU", () => {
    const [row] = mapMarginPreviewItems([{
      sku: "WB-900",
      revenue: "100",
      marketplace_fees: "20",
      cost_price: "60",
      margin: "20",
      margin_percent: "20",
      calculation_status: "complete",
    }]);

    expect(row.product).toBe("Товар WB-900");
    expect(row.status).toBe("attention");
  });


  it("keeps missing cost as an incomplete row", () => {
    const [row] = mapMarginPreviewItems([{
      sku: "WB-404",
      revenue: "1000",
      marketplace_fees: "200",
      cost_price: null,
      margin: null,
      margin_percent: null,
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
      { sku: "A", product: "A", revenue: 100, fees: 20, cost: 70, margin: 10, percent: 10, status: "critical" },
      { sku: "B", product: "B", revenue: 900, fees: 90, cost: 360, margin: 450, percent: 50, status: "healthy" },
      { sku: "C", product: "C", revenue: 500, fees: 50, cost: null, margin: null, percent: null, status: "incomplete" },
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
