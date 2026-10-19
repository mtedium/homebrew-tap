cask "irightmouse-pro" do
  version "2.5.1"
  sha256 "11932159dbf07b80244d50a597cba6b7437f4ba6240b385d6f76dc8fe5f9dfd0"

  url "https://download.s21i.co99.net/33780428/0/0/ABUIABBtGAAgxvLj1QYo0rWu6gc.dmg?f=iRightMousePro2.5.1_2026092701.dmg&v=1790507340"
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
