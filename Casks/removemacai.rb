cask "removemacai" do
  version "1.2.0"
  sha256 "574ebc7475efb95e6d911b53f63f45efbb5b03cbcb2ba1e48736a329a908ccca"

  url "https://github.com/omlahore/RemoveMacAI/releases/download/v1.2.0/RemoveMacAI.zip"
  name "RemoveMacAI"
  desc "Manage Apple Intelligence, privacy settings and storage cleanup"
  homepage "https://github.com/omlahore/RemoveMacAI"

  depends_on arch: :arm64
  depends_on macos: :tahoe

  app "RemoveMacAI.app"
end
