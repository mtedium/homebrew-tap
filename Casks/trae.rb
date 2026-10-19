cask "trae" do
  version "3.6.4"
  sha256 "0bf501b0ce59332f694c98ca0e0061c270672e5767241da7a6c529db3b5a8163"

  url "https://lf-cdn.trae.ai/obj/trae-ai-us/pkg/app/releases/stable/2.3.93439/darwin/TRAE-darwin-arm64.dmg"
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
