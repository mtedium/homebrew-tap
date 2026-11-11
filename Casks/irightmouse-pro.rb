cask "irightmouse-pro" do
  version "2.5.1"
  sha256 "f4b88ee88b7d43e0d3affbbc35b7a6feefab97f8647bb7fadfa970e086a77308"

  url "https://download.s21i.co99.net/33780428/0/0/ABUIABBtGAAgyujF1wYo_aH9Cw.dmg?f=iRightMousePro_2.5.1_2026110701.dmg&v=1794208847"
  name "iRightMouse Pro"
  name "超级右键专业版"
  desc "Finder context menu tools"
  homepage "https://www.aodo365.com/irightmousepro.html"

  livecheck do
    url :homepage
    regex(/>\s*v(\d+(?:\.\d+)+)\s*</i)
    strategy :page_match
  end

  app "iRightMouse Pro.app"
end
