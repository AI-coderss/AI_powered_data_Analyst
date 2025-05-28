import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import HighchartsHeatmap from "highcharts/modules/heatmap";
import HighchartsDrilldown from "highcharts/modules/drilldown";
import "../styles/Dashboard.css";

export default function Dashboard({ charts }) {
  if (!charts || charts.length === 0) return <p>No charts to display</p>;

  return (
    <div className="dashboard-container">
      <div className="chart-wrapper">
        {charts.map((options, i) => (
          <HighchartsReact key={i} highcharts={Highcharts} options={options} />
        ))}
      </div>
    </div>
  );
}
