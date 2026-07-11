#define SourceRoot "..\.."
#define OutputRoot "..\..\nova website\downloads"
#define AppVersion "1.1.0"

[Setup]
AppId={{BC7B01F6-5E35-4C4C-9B56-A29D76908B1A}
AppName=NovaDev
AppVersion={#AppVersion}
AppPublisher=NovaDev
AppPublisherURL=https://novadev-org.vercel.app/
AppSupportURL=https://novadev-org.vercel.app/
AppUpdatesURL=https://novadev-org.vercel.app/
DefaultDirName={localappdata}\NovaDev
DefaultGroupName=NovaDev
DisableProgramGroupPage=yes
OutputDir={#OutputRoot}
OutputBaseFilename=NovaDevSetup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest
ChangesEnvironment=yes
ChangesAssociations=yes
WizardStyle=modern
SetupIconFile=assets\novadev.ico
WizardSmallImageFile=assets\novadev-small.bmp
WizardImageFile=assets\novadev-wizard.bmp
UninstallDisplayIcon={app}\assets\novadev.ico

[Tasks]
Name: "desktopicon"; Description: "Create a NovaDev Manager desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked
Name: "vscodeextension"; Description: "Install NovaDev VS Code language and icon support"; GroupDescription: "Editor integration:"

[Dirs]
Name: "{app}\bin"
Name: "{app}\cache"
Name: "{app}\packages"

[Files]
Source: "{#SourceRoot}\*"; DestDir: "{app}\language"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: ".git\*,.novadev\*,.venv\*,__pycache__\*,.pytest_cache\*,node_modules\*,generated\*,generated_backend\*,generated_backend_*\*,generated_docs_webshield\*,generated_notes\*,generated_project\*,generated_projects\*,dist\*,dist_ecommerce\*,.tmp-*\*,nova website\downloads\*.zip,nova website\downloads\*.exe"
Source: "bin\find-python.cmd"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "bin\nova.cmd"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "bin\nova-shell.cmd"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "bin\novapm.cmd"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "bin\novadev-manager.cmd"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "bin\novadev-manager.vbs"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "assets\novadev.ico"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\novadev-small.bmp"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\novadev-wizard.bmp"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\novadev-logo.svg"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "{#SourceRoot}\tools\vscode\novadev\*"; DestDir: "{%USERPROFILE}\.vscode\extensions\novadev.novadev-language-1.1.0"; Flags: ignoreversion recursesubdirs createallsubdirs; Tasks: vscodeextension
Source: "{#SourceRoot}\packages\hello-ui\*"; DestDir: "{app}\packages\hello-ui@0.1.0"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourceRoot}\packages\auth-kit\*"; DestDir: "{app}\packages\auth-kit@0.1.0"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourceRoot}\packages\dashboard-kit\*"; DestDir: "{app}\packages\dashboard-kit@0.1.0"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\NovaDev Manager"; Filename: "{sys}\wscript.exe"; Parameters: """{app}\bin\novadev-manager.vbs"""; WorkingDir: "{app}\language"; IconFilename: "{app}\assets\novadev.ico"
Name: "{group}\NovaDev Shell"; Filename: "{app}\bin\nova.cmd"; Parameters: "shell"; WorkingDir: "{app}\language"; IconFilename: "{app}\assets\novadev.ico"
Name: "{group}\NovaDev Package Manager Doctor"; Filename: "{app}\bin\novapm.cmd"; Parameters: "doctor"; WorkingDir: "{app}\language"; IconFilename: "{app}\assets\novadev.ico"
Name: "{userdesktop}\NovaDev Manager"; Filename: "{sys}\wscript.exe"; Parameters: """{app}\bin\novadev-manager.vbs"""; WorkingDir: "{app}\language"; IconFilename: "{app}\assets\novadev.ico"; Tasks: desktopicon

[Registry]
Root: HKCU; Subkey: "Software\Classes\.nova"; ValueType: string; ValueName: ""; ValueData: "NovaDev.SourceFile"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Classes\NovaDev.SourceFile"; ValueType: string; ValueName: ""; ValueData: "NovaDev Source File"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\NovaDev.SourceFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\assets\novadev.ico,0"
Root: HKCU; Subkey: "Software\Classes\NovaDev.SourceFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\bin\nova.cmd"" run ""%1"""
Root: HKCU; Subkey: "Software\Classes\NovaDev.SourceFile\shell\edit\command"; ValueType: string; ValueName: ""; ValueData: "notepad.exe ""%1"""

[Run]
Filename: "{sys}\wscript.exe"; Parameters: """{app}\bin\novadev-manager.vbs"""; Description: "Launch NovaDev Manager"; Flags: nowait postinstall skipifsilent

[Code]
const
  RegistryUrl = 'https://novadev-org.vercel.app/downloads/registry.json';

function JsonEscape(Value: String): String;
begin
  Result := Value;
  StringChangeEx(Result, '\', '\\', True);
  StringChangeEx(Result, '"', '\"', True);
end;

function PathContains(PathValue: String; Dir: String): Boolean;
var
  Haystack: String;
  Needle: String;
begin
  Haystack := ';' + Lowercase(PathValue) + ';';
  Needle := ';' + Lowercase(Dir) + ';';
  Result := Pos(Needle, Haystack) > 0;
end;

procedure AddToUserPath(Dir: String);
var
  CurrentPath: String;
  NewPath: String;
begin
  if not RegQueryStringValue(HKCU, 'Environment', 'Path', CurrentPath) then
    CurrentPath := '';

  if PathContains(CurrentPath, Dir) then
    exit;

  if CurrentPath = '' then
    NewPath := Dir
  else
    NewPath := CurrentPath + ';' + Dir;

  RegWriteStringValue(HKCU, 'Environment', 'Path', NewPath);
end;

procedure WriteConfig;
var
  Config: String;
begin
  Config := '{' + #13#10 +
    '  "registry": "' + RegistryUrl + '"' + #13#10 +
    '}' + #13#10;
  SaveStringToFile(ExpandConstant('{app}\config.json'), Config, False);
end;

procedure WriteInstalledPackages;
var
  AppDir: String;
  Json: String;
begin
  AppDir := JsonEscape(ExpandConstant('{app}'));
  Json := '{' + #13#10 +
    '  "packages": {' + #13#10 +
    '    "hello-ui": {' + #13#10 +
    '      "name": "hello-ui",' + #13#10 +
    '      "version": "0.1.0",' + #13#10 +
    '      "description": "Example NovaDev UI helpers and starter page declarations.",' + #13#10 +
    '      "path": "' + AppDir + '\\packages\\hello-ui@0.1.0",' + #13#10 +
    '      "kind": "module"' + #13#10 +
    '    },' + #13#10 +
    '    "auth-kit": {' + #13#10 +
    '      "name": "auth-kit",' + #13#10 +
    '      "version": "0.1.0",' + #13#10 +
    '      "description": "Starter auth declarations for NovaDev apps.",' + #13#10 +
    '      "path": "' + AppDir + '\\packages\\auth-kit@0.1.0",' + #13#10 +
    '      "kind": "module"' + #13#10 +
    '    },' + #13#10 +
    '    "dashboard-kit": {' + #13#10 +
    '      "name": "dashboard-kit",' + #13#10 +
    '      "version": "0.1.0",' + #13#10 +
    '      "description": "Reusable dashboard page declarations and UI helpers.",' + #13#10 +
    '      "path": "' + AppDir + '\\packages\\dashboard-kit@0.1.0",' + #13#10 +
    '      "kind": "module"' + #13#10 +
    '    }' + #13#10 +
    '  }' + #13#10 +
    '}' + #13#10;
  SaveStringToFile(ExpandConstant('{app}\installed.json'), Json, False);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    WriteConfig;
    WriteInstalledPackages;
    AddToUserPath(ExpandConstant('{app}\bin'));
  end;
end;
