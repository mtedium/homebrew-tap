cask "removemacai" do
  version "1.1.4"
  sha256 "2063d4dc7e0b41b15cebcd9e1b9807b04615b96e3e23db35cbd1196be3c96bee"

  url "https://github.com/omlahore/RemoveMacAI/releases/download/v1.1.4/RemoveMacAI.zip"
  name "RemoveMacAI"
  desc "Manage Apple Intelligence, privacy settings and storage cleanup"
  homepage "https://github.com/omlahore/RemoveMacAI"

  depends_on arch: :arm64
  depends_on macos: ">= :tahoe"

  app "RemoveMacAI.app"
end
