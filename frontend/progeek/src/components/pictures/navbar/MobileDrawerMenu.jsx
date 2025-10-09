import React from "react";
import Drawer from "@mui/joy/Drawer";
import List from "@mui/joy/List";
import ListItem from "@mui/joy/ListItem";
import ListItemButton from "@mui/joy/ListItemButton";
import ListItemContent from "@mui/joy/ListItemContent";
import Box from "@mui/joy/Box";
import Skeleton from "@mui/joy/Skeleton";
import ColorModeSwitcher from "./ColorModeSwitcher";
import { Link } from "react-router-dom";

export default function MobileDrawerMenu({ open, onClose, navLinks }) {
  const [loading, setLoading] = React.useState(true);
  React.useEffect(() => {
    if (open) {
      setLoading(true);
      const t = setTimeout(() => setLoading(false), 350);
      return () => clearTimeout(t);
    } else {
      setLoading(true);
    }
  }, [open]);

  const theme = ColorModeSwitcher?.theme || {};
  const isDark = theme?.palette?.mode === "dark";

  return (
    <Drawer
      open={open}
      onClose={onClose}
      anchor="right"
      aria-label="Navigációs menü"
      slotProps={{
        content: {
          sx: {
            bgcolor: isDark ? "#181828" : "#fff",
            color: isDark ? "#fff" : "#181828",
            overflow: "visible",
            transition:
              "box-shadow 0.25s cubic-bezier(.4,2,.6,1), background 0.18s",
          },
        },
      }}
    >
      <Box
        sx={{
          p: 2,
          display: "flex",
          flexDirection: "column",
          gap: 2,
          alignItems: "center",
          overflow: "visible",
          transition:
            "box-shadow 0.25s cubic-bezier(.4,2,.6,1), background 0.18s",
        }}
      >
        <Box
          sx={{
            p: 0,
            mb: 1,
            borderRadius: "50%",
            overflow: "visible",
            background: "none !important",
            boxShadow: "none !important",
            border: "none !important",
            minWidth: 0,
            minHeight: 0,
            width: "auto",
            height: "auto",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          {loading ? (
            <Skeleton
              variant="circular"
              width={40}
              height={40}
              sx={{ bgcolor: "#222", m: 0 }}
            />
          ) : (
            <ColorModeSwitcher />
          )}
        </Box>
        <List
          sx={{
            minWidth: 180,
            bgcolor: "transparent",
            color: isDark ? "#fff" : "#181828",
            boxShadow: "none",
            p: 0,
          }}
        >
          {loading
            ? Array.from({ length: navLinks.length }).map((_, i) => (
                <ListItem key={i} sx={{ p: 0, m: 0, bgcolor: "transparent", boxShadow: "none" }}>
                  <Skeleton
                    variant="rectangular"
                    width={120}
                    height={32}
                    sx={{
                      borderRadius: 8,
                      bgcolor: "#222",
                      m: 0,
                    }}
                  />
                </ListItem>
              ))
            : navLinks.map((link) => (
                <ListItem key={link.to} sx={{ p: 0, m: 0, bgcolor: "transparent", boxShadow: "none" }}>
                  <ListItemButton
                    component={Link}
                    to={link.to}
                    onClick={onClose}
                    aria-label={link.label}
                    sx={{
                      bgcolor: "transparent",
                      color: "text.primary",
                      boxShadow: "none",
                      borderRadius: 0,
                      p: 0,
                      m: 0,
                      minHeight: 40,
                      fontWeight: 600,
                      fontSize: 18,
                      justifyContent: "center",
                      '&:hover': {
                        bgcolor: 'primary.500',
                        color: 'background.body',
                      },
                    }}
                  >
                    <ListItemContent sx={{ p: 0, m: 0 }}>{link.label}</ListItemContent>
                  </ListItemButton>
                </ListItem>
              ))}
        </List>
      </Box>
    </Drawer>
  );
}
