// Writes one SVG glyph per hardware.html family, drawn by the app's own
// TabletFigure code so the page and the app's orientation picker match.
//
// Run through export.sh, which compiles this against the app's sources.
// It also writes light and dark copies of each family, plus each entry in
// `extraGlyphs`, for pages that can't style an SVG, like a GitHub README.
//
// Arguments: devices.json, registry.json, the output folder, the folder for
// light and dark copies, then optional extra `slug=0xPID` pairs.

import CoreGraphics
import Foundation

struct Family {
    var slug: String
    var productID: Int
    var surfaceMM: CGSize?
    var isPenDisplay: Bool?
    /// Written only as light and dark copies.
    var variantsOnly = false
}

func hex(_ s: String) -> Int? { Int(s.hasPrefix("0x") ? String(s.dropFirst(2)) : s, radix: 16) }

func json(_ path: String) -> Any {
    guard let data = FileManager.default.contents(atPath: path),
          let value = try? JSONSerialization.jsonObject(with: data)
    else { fatalError("can't read \(path)") }
    return value
}

let args = CommandLine.arguments
guard args.count >= 5 else {
    FileHandle.standardError.write(Data("usage: export devices.json registry.json OUTDIR VARIANTDIR [slug=0xPID ...]\n".utf8))
    exit(2)
}
let devices = json(args[1]) as! [String: Any]
let registryJSON = json(args[2])
let registryRows = (registryJSON as? [[String: Any]]) ?? ((registryJSON as! [String: Any])["devices"] as! [[String: Any]])
let outDir = URL(fileURLWithPath: args[3], isDirectory: true)
let variantDir = URL(fileURLWithPath: args[4], isDirectory: true)
/// GitHub's muted text in its light and dark themes.
let variantInk = ["light": "#59636e", "dark": "#9198a1"]

var registry: [Int: [String: Any]] = [:]
for row in registryRows {
    let pid = (row["productID"] as? Int) ?? hex(row["productID"] as! String)!
    registry[pid] = row
}

var families: [Family] = []
for (key, variantsOnly) in [("families", false), ("extraGlyphs", true)] {
    for (slug, value) in (devices[key] as? [String: [String: Any]] ?? [:]).sorted(by: { $0.key < $1.key }) {
        var family = Family(slug: slug, productID: hex(value["glyph"] as! String)!, variantsOnly: variantsOnly)
        if let mm = value["surfaceMM"] as? [Double] { family.surfaceMM = CGSize(width: mm[0], height: mm[1]) }
        family.isPenDisplay = value["penDisplay"] as? Bool
        families.append(family)
    }
}
for extra in args.dropFirst(5) {
    let pair = extra.split(separator: "=")
    families.append(Family(slug: String(pair[0]), productID: hex(String(pair[1]))!))
}

/// A rounded rectangle as an SVG subpath, clockwise from the top left.
func roundedRect(_ r: CGRect, _ radius: Double) -> String {
    let k = min(radius, min(r.width, r.height) / 2)
    func n(_ v: Double) -> String {
        let s = String(format: "%.2f", v)
        return s.replacingOccurrences(of: #"\.?0+$"#, with: "", options: .regularExpression)
    }
    if k <= 0 { return "M\(n(r.minX)) \(n(r.minY))h\(n(r.width))v\(n(r.height))h\(n(-r.width))z" }
    return "M\(n(r.minX + k)) \(n(r.minY))h\(n(r.width - 2 * k))a\(n(k)) \(n(k)) 0 0 1 \(n(k)) \(n(k))"
        + "v\(n(r.height - 2 * k))a\(n(k)) \(n(k)) 0 0 1 \(n(-k)) \(n(k))"
        + "h\(n(-(r.width - 2 * k)))a\(n(k)) \(n(k)) 0 0 1 \(n(-k)) \(n(-k))"
        + "v\(n(-(r.height - 2 * k)))a\(n(k)) \(n(k)) 0 0 1 \(n(k)) \(n(-k))z"
}

/// The glyph as one even-odd path: the outline ring, the filled panels, and
/// the controls knocked out of them, matching TabletFigureInk's radii.
func svg(_ figure: TabletFigure, fill: String = "currentColor") -> String {
    let d = figure.drawing(.glyph, in: CGRect(x: 0, y: 0, width: 100, height: 100), scale: 2)
    let origin = d.body.origin
    func local(_ r: CGRect) -> CGRect { r.offsetBy(dx: -origin.x, dy: -origin.y) }
    var path = [roundedRect(local(d.body), 7), roundedRect(local(d.opening), 4)]
    path += (d.bands + [d.surface]).map { roundedRect(local($0), 2) }
    for shape in d.shapes {
        let r = local(shape.rect)
        switch shape.kind {
        case .ring, .dial: path.append(roundedRect(r, r.width / 2))
        case .strip: path.append(roundedRect(r, min(r.width, r.height) / 2))
        case .key, .cluster: path.append(roundedRect(r, 1))
        case .mark: path.append(roundedRect(r, 0))
        }
    }
    let w = Int(d.body.width.rounded()), h = Int(d.body.height.rounded())
    return """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 \(w) \(h)" width="\(w / 2)" height="\(h / 2)" aria-hidden="true" focusable="false"><path fill="\(fill)" fill-rule="evenodd" d="\(path.joined())"/></svg>

    """
}

try FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)
try FileManager.default.createDirectory(at: variantDir, withIntermediateDirectories: true)
for family in families {
    let row = registry[family.productID]
    let mm = family.surfaceMM ?? {
        guard let w = row?["activeWidthMM"] as? Double, let h = row?["activeHeightMM"] as? Double else { return nil }
        return CGSize(width: w, height: h)
    }()
    let figure = TabletFigure(
        layoutProductID: row == nil ? nil : family.productID, surfaceMM: mm,
        aspect: mm.map { $0.width / $0.height } ?? 1.5,
        isPenDisplay: family.isPenDisplay ?? (row?["isPenDisplay"] as? Bool ?? false))
    if !family.variantsOnly {
        try svg(figure).write(to: outDir.appendingPathComponent("\(family.slug).svg"), atomically: true, encoding: .utf8)
    }
    for (scheme, ink) in variantInk {
        let file = variantDir.appendingPathComponent("\(family.slug)-\(scheme).svg")
        try svg(figure, fill: ink).write(to: file, atomically: true, encoding: .utf8)
    }
    print("\(family.slug): 0x\(String(format: "%04X", family.productID)) \(row?["name"] as? String ?? "(not in registry)")")
}
