// theme.light.js for Joy UI (MUI) custom theme
import { extendTheme } from "@mui/joy/styles";

const lightTheme = extendTheme({
  colorSchemes: {
    light: {
      palette: {
        background: {
          body: "#fff",
        },
        text: {
          primary: "#000",
        },
        primary: {
          500: "#50C3D0",
        },
        secondary: {
          500: "#9E7BE2",
        },
      },
    },
  },
  fontFamily: {
    body: "Inter, sans-serif",
    display: "Inter, sans-serif",
  },
});

export default lightTheme;
