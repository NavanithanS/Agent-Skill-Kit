class AgentSkillKit < Formula
  include Language::Python::Virtualenv

  desc "CLI package manager for AI agent skills — deploy skills to Claude, Gemini, Codex, Cursor, and more"
  homepage "https://navanithans.github.io/Agent-Skill-Kit/"
  url "https://files.pythonhosted.org/packages/source/a/agent-skill-kit/agent_skill_kit-0.6.0.tar.gz"
  sha256 "FILL_IN_AFTER_PYPI_PUBLISH"
  license "MIT"
  version "0.6.0"

  depends_on "python@3.12"

  resource "click" do
    url "https://files.pythonhosted.org/packages/source/c/click/click-8.1.8.tar.gz"
    sha256 "ed53c9d8821d0d21f5f86cd51f030a1ef851cd73af68f4f2dfd4fe41d9b7c6b0"
  end

  resource "pyyaml" do
    url "https://files.pythonhosted.org/packages/source/P/PyYAML/PyYAML-6.0.2.tar.gz"
    sha256 "d584d9ec91ad65861cc08d42e834324ef890a082e591037abe114850ff7bbc3e"
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/source/r/rich/rich-13.9.4.tar.gz"
    sha256 "439594978a49a09530cff7ebc4b5c7103ef57baf48d5ea3184f21d9a2befa098"
  end

  resource "markdown-it-py" do
    url "https://files.pythonhosted.org/packages/source/m/markdown-it-py/markdown_it_py-3.0.0.tar.gz"
    sha256 "e3f60a94fa066dc52ec76661e37c851cb232d92f9886b15cb560aaada2df8feb"
  end

  resource "mdurl" do
    url "https://files.pythonhosted.org/packages/source/m/mdurl/mdurl-0.1.2.tar.gz"
    sha256 "bb413d29f5eea38f31dd4754dd7377d4465116fb207585f97bf925588687c1ba"
  end

  resource "pygments" do
    url "https://files.pythonhosted.org/packages/source/p/pygments/pygments-2.18.0.tar.gz"
    sha256 "786ff802f32e91311bff3889f6e9a86e81505fe99f2735bb6d60ae0c5004f199"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "0.6.0", shell_output("#{bin}/ask --version")
    assert_match "copy", shell_output("#{bin}/ask --help")
  end
end
