cask "trae" do
  version "3.6.24"
  sha256 "12b1160a512d14c4239703aec6d4eb28056be524ff8004991d87d6c502508861"

  url "https://lf-cdn.trae.ai/obj/trae-ai-us/pkg/app/releases/stable/2.3.106769/darwin/TRAE-darwin-arm64.dmg"
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
