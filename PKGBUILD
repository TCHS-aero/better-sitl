# Maintainer: Matthew Hannon <matthannon.dev@gmail.com>
pkgname=better-sitl
pkgver=1.0.2
pkgrel=1
pkgdesc="A Python CLI wrapper built with click for PX4's SIH and Gazebo SITL docker images; designed for a smoother integrated workflow."
arch=('any')
url="https://github.com/TCHS-aero/better-sitl"
license=('MIT')
depends=('python>=3.12' 'python-click')
makedepends=('python-build' 'python-installer' 'python-setuptools')
optdepends=('docker: run the SITL simulator containers')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
    cd "$pkgname-$pkgver"
    python -m build --wheel --no-isolation
}

package() {
    cd "$pkgname-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
