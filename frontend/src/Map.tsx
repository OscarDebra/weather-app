import {
  ComposableMap,
  Geographies,
  Geography,
} from "react-simple-maps";

const geoUrl =
  "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";

export default function WorldMapPage() {
  return (
    <div>
      <h2>World Map</h2>

      <ComposableMap>
        <Geographies geography={geoUrl}>
          {({ geographies }) =>
            geographies.map((geo) => (
              <Geography
                key={geo.rsmKey}
                geography={geo}
                style={{
                  default: { fill: "#D6D6DA", outline: "none" },
                  hover: { fill: "#999", outline: "none" },
                  pressed: { fill: "#555", outline: "none" },
                }}
              />
            ))
          }
        </Geographies>
      </ComposableMap>
    </div>
  );
}