# Minecraft Realms Emulator

This is a custom implementation of a Minecraft Realms server for Java Edition.

**🚀 Now Available in Two Versions:**
- **C# (ASP.NET Core)** - Original implementation (see instructions below)
- **Python (FastAPI)** - New Python port (see [README_PYTHON.md](README_PYTHON.md))

# Requirements (C# Version)

- .NET SDK (version 8.0 or higher)
- Minecraft Java Edition
- PostgreSQL (for database support)
- Docker (for `REALMS` mode to work)

**For Python version requirements, see [README_PYTHON.md](README_PYTHON.md)**

# Installation (C# Version)

Clone the repository:

```sh
git clone https://github.com/CyberL1/Minecraft-Realms-Emulator.git 
cd Minecraft-Realms-Emulator/Minecraft-Realms-Emulator
```

Configure the server:

Create a `.env` file:

```
CONNECTION_STRING="User Id=postgres;Password=password;Server=db;Port=5432;Database=Minecraft-Realms-Emulator;"
ADMIN_KEY="[RANDOMLY GENERATED KEY]"
```

Build the server:

```sh
dotnet build
```

Run the server:

```sh
dotnet run
```

# Demo

[![Demo](https://img.youtube.com/vi/5pHPsKQhEjI/0.jpg)](https://www.youtu.be/5pHPsKQhEjI)
