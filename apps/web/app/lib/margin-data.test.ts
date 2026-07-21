import { describe, expect, it } from "vitest";

import { getMarginStatus, mapMarginPreviewItems } from "./margin-data";

describe("getMarginStatus", () => {
  it.each([
    [19.99, "critical"],
    [20, "attention"],
    [24.99, "attention"],
    [25, "healthy"],
  ] as const)("assigns %s%% to %s", (percent, expected) => {
    expect(getMarginStatus(percent)).toBe(expected);
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
    }]);

    expect(row.product).toBe("Товар WB-900");
    expect(row.status).toBe("attention");
  });
});
