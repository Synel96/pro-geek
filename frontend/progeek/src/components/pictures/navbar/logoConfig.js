// logoConfig.js

export const LOGO_GLOW = `
  drop-shadow(-6px 0 10px #50C3D0)
  drop-shadow(6px 0 18px #9E7BE2)
  drop-shadow(0 0 24px #9E7BE2)
`;

export const LOGO_EMBOSS = `
  1px 1px 1px rgba(255,255,255,0.6),  /* felső fény */
  -1px -1px 2px rgba(0,0,0,0.5)       /* alsó árnyék */
`;

export const LOGO_PADDING = (isMobile) => (isMobile ? 2 : 4);
export const LOGO_SIZE = (isMobile) => (isMobile ? 120 : 160);
