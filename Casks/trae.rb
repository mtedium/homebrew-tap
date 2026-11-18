cask "trae" do
  version "3.6.20"
  sha256 "99f40750eaf9674088cdb25757dab8ca64101c2a7dbff526786830cfbb745ef9"

  url "https://lf-cdn.trae.ai/obj/trae-ai-us/pkg/app/releases/stable/2.3.103560/darwin/TRAE-darwin-arm64.dmg"
  name "TRAE"
  desc "AI-powered code editor"
  homepage "https://www.trae.ai/"

  livecheck do
    url "https://api.trae.ai/icube/api/v1/native/version/trae/latest"
    strategy :json do |json|
      json.dig("data", "manifest", "darwin", "versions")
          &.find { |release| release["region"] == "va" && release["arch"] == "apple" }
          &.fetch("version")
    end
  end

  depends_on arch: :arm64
  depends_on macos: :monterey

  app "Trae.app"
end
