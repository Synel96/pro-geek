import React from "react";
import Button from "@mui/joy/Button";
import { useColorScheme } from "@mui/joy/styles";
import { useTheme } from "@mui/joy/styles";
import { MENU_GLOW_DARK, MENU_GLOW_LIGHT } from "./menuButtonGlow";

export default function MenuButton({ children, ...props }) {
  const { mode } = useColorScheme();
  const theme = useTheme();
  const [hover, setHover] = React.useState(false);
  const glow = mode === "dark" ? MENU_GLOW_DARK : MENU_GLOW_LIGHT;
  return (
    <Button
      variant="plain"
      sx={{
        fontWeight: 600,
        fontFamily: theme.fontFamily?.body || "Inter, sans-serif",
        bgcolor: mode === "dark" ? "#000" : "#fff",
        color: mode === "dark" ? "#fff" : "#000",
        borderRadius: 2,
        px: 2.5,
        py: 1,
        boxShadow: hover ? glow : "none",
        transition: "background 0.18s, color 0.18s, box-shadow 0.18s",
        "&:hover": {
          bgcolor: mode === "dark" ? "#222" : "#eee",
          color: mode === "dark" ? "#50C3D0" : "#9E7BE2",
        },
      }}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      onFocus={() => setHover(true)}
      onBlur={() => setHover(false)}
      {...props}
    >
      {children}
    </Button>
  );
}
