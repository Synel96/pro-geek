import React from "react";
import Box from "@mui/joy/Box";
import Typography from "@mui/joy/Typography";
import Sheet from "@mui/joy/Sheet";
import { useTheme } from "@mui/joy/styles";
import InputField from "../forms/InputField";
import SubmitButton from "../forms/SubmitButton";

export default function LoginWindow() {
  const theme = useTheme();
  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "flex-start",
        justifyContent: "center",
        bgcolor: "background.body",
        pt: { xs: 8, sm: 12 },
      }}
    >
      <Sheet
        variant="outlined"
        sx={{
          p: 4,
          borderRadius: 3,
          minWidth: 320,
          boxShadow:
            "0 0 0 4px rgba(120,60,220,0.32), 0 8px 40px 0 rgba(120,60,220,0.38)",
          bgcolor: "background.surface",
          display: "flex",
          flexDirection: "column",
          gap: 2,
          border: "2px solid",
          borderColor: "secondary.500",
          transition:
            "box-shadow 0.22s cubic-bezier(.4,2,.6,1), transform 0.22s cubic-bezier(.4,2,.6,1)",
          willChange: "box-shadow, transform",
          "&:hover": {
            boxShadow:
              "0 0 0 6px rgba(120,60,220,0.38), 0 16px 56px 0 rgba(120,60,220,0.44)",
            transform: "translateY(-6px) scale(1.03)",
          },
        }}
      >
        <Typography
          level="h4"
          sx={{
            color: "text.primary",
            mb: 1,
            fontWeight: 700,
            fontFamily: "var(--joy-fontFamily-body, inherit)",
          }}
        >
          Bejelentkezés
        </Typography>
        <InputField
          placeholder="Felhasználónév"
          type="text"
          name="username"
          autoComplete="username"
        />
        <InputField
          placeholder="Jelszó"
          type="password"
          name="password"
          autoComplete="current-password"
        />
        <SubmitButton
          variant="solid"
          color="primary"
          sx={{
            mt: 2,
            fontWeight: 600,
            fontFamily: "var(--joy-fontFamily-body, inherit)",
          }}
          fullWidth
        >
          Belépés
        </SubmitButton>
        <SubmitButton
          variant="plain"
          color="secondary"
          sx={{
            mt: 1,
            fontWeight: 500,
            fontFamily: "var(--joy-fontFamily-body, inherit)",
            color: "text.primary",
          }}
          fullWidth
        >
          Elfelejtett jelszó?
        </SubmitButton>
        <Typography
          level="body2"
          sx={{
            mt: 3,
            color: "text.secondary",
            textAlign: "center",
            fontFamily: "var(--joy-fontFamily-body, inherit)",
            cursor: "pointer",
          }}
        >
          Van már regisztrációs kódod?{" "}
          <span
            style={{
              color: "#783cdc",
              textDecoration: "underline",
              cursor: "pointer",
            }}
          >
            Regisztrálj itt!
          </span>
        </Typography>
      </Sheet>
    </Box>
  );
}
