cask "removemacai" do
  version "1.2.2"
  sha256 "320bfe3c5b8dab3ace082ffa5be3e242d11a56d9218699219211651e605f9b90"

  url "https://github.com/omlahore/RemoveMacAI/releases/download/v1.2.2/RemoveMacAI.zip"
  name "RemoveMacAI"
  desc "Manage Apple Intelligence, privacy settings and storage cleanup"
  homepage "https://github.com/omlahore/RemoveMacAI"

  depends_on arch: :arm64
  depends_on macos: :tahoe

  app "RemoveMacAI.app"
end
