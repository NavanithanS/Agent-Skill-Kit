class AgentSkillKit < Formula
  desc "CLI package manager for AI agent skills — deploy to Claude, Gemini, Codex, Cursor, and more"
  homepage "https://navanithans.github.io/Agent-Skill-Kit/"
  url "https://pypi.io/packages/source/a/agent-skill-kit/agent_skill_kit-0.10.1.tar.gz"
  sha256 "794de51f585c2ec555c4a6e75d374bc9fd0ee78c42fb39227389f0a263c6882e"
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
