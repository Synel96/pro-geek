// logoAssets.js
// Vite-imagetools import szintaxis: import logo from '../../public/logo.png?w=400;webp;avif'
// A public mappából NEM működik, ezért tedd át a logo.png-t a src/assets-be!

import logoSrcSet from "../../../assets/logo.png?w=400;webp;avif&as=srcset";
import logoPng from "../../../assets/logo.png?w=400&as=src";

export { logoSrcSet, logoPng };
