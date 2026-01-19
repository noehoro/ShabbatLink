import type { NextConfig } from "next";
import path from 'path';

const nextConfig: NextConfig = {
  output: 'standalone',
  experimental: {
    turbo: {
      resolveAlias: {
        '@/*': ['./*'],
      },
    },
  },
};

export default nextConfig;
