cask "trae" do
  version "3.6.13"
  sha256 "2644135f0e783c6a2f5860b8e8fdae9c0a72cbb1fe935d1e4bf022812ca04452"

  url "https://lf-cdn.trae.ai/obj/trae-ai-us/pkg/app/releases/stable/2.3.99397/darwin/TRAE-darwin-arm64.dmg"
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
