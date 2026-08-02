class AgentSkillKit < Formula
  desc "CLI package manager for AI agent skills — deploy to Claude, Gemini, Codex, Cursor, and more"
  homepage "https://navanithans.github.io/Agent-Skill-Kit/docs/"
  url "https://pypi.io/packages/source/a/agent-skill-kit/agent_skill_kit-0.9.1.tar.gz"
  sha256 "5176f858450eeafda05a444b13f686fb181aa98558140dd6769aca07f8565430"
  license "MIT"

  depends_on "python@3.12"

  def install
    # Create a virtual environment in the libexec directory
    system "python3", "-m", "venv", libexec
    
    # Install the package and its dependencies into the virtual environment
    # This assumes the machine has internet access during the build (standard for private taps)
    system libexec/"bin/pip", "install", "-v", "."
    
    # Symlink the 'ask' executable to the bin directory
    bin.install_symlink libexec/"bin/ask"
  end

  test do
    # Verify the installation by checking the version
    system "#{bin}/ask", "--version"
  end
end
