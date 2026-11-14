import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["src/**/*.unit.test.ts"],
    environment: "node",

    coverage: {
      provider: "v8",

      include: [
        "src/utils/productSearch.ts"
      ],

      reporter: [
        "text",
        "html",
        "lcov"
      ],

      thresholds: {
        statements: 80,
        branches: 80,
        functions: 80,
        lines: 80
      }
    }
  }
});