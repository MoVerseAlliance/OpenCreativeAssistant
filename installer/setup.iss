; Inno Setup 脚本 for OpenCreativeAssistant
[Setup]
AppName=OpenCreativeAssistant
AppVersion=1.0
AppPublisher=YourName
AppPublisherURL=https://example.com
DefaultDirName={autopf}\OpenCreativeAssistant
DefaultGroupName=OpenCreativeAssistant
OutputDir=C:\Users\juezhan2026\Desktop\DCC\installer
OutputBaseFilename=OpenCreativeAssistant_Setup
Compression=lzma
SolidCompression=yes
UninstallDisplayIcon={app}\main.exe
WizardStyle=modern

[Files]
Source: "C:\Users\juezhan2026\Desktop\DCC\dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\juezhan2026\Desktop\DCC\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs
Source: "C:\Users\juezhan2026\Desktop\DCC\src\config.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\OpenCreativeAssistant"; Filename: "{app}\main.exe"
Name: "{commondesktop}\OpenCreativeAssistant"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,OpenCreativeAssistant}"; Flags: nowait postinstall skipifsilent
