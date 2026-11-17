cask "removemacai" do
  version "1.2.1"
  sha256 "f1d17285be5d955141f7692939c07994351ebd3f41afc5ae7ff5d1f3253011f5"

  url "https://github.com/omlahore/RemoveMacAI/releases/download/v1.2.1/RemoveMacAI.zip"
  name "RemoveMacAI"
  desc "Manage Apple Intelligence, privacy settings and storage cleanup"
  homepage "https://github.com/omlahore/RemoveMacAI"

  depends_on arch: :arm64
  depends_on macos: :tahoe

  app "RemoveMacAI.app"
end
