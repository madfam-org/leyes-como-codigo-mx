import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  transpilePackages: ['@leyesmx/ui', '@leyesmx/lib'],
};

export default nextConfig;
