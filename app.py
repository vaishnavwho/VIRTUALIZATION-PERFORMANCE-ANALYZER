from textwrap import dedent

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


DEFAULT_DATA = {
    "VMware": {
        "CPU Usage (%)": 38.0,
        "RAM Usage (GB)": 4.2,
        "Disk Performance (MB/s)": 245.0,
        "Boot Time (seconds)": 28.0,
    },
    "VirtualBox": {
        "CPU Usage (%)": 46.0,
        "RAM Usage (GB)": 4.8,
        "Disk Performance (MB/s)": 205.0,
        "Boot Time (seconds)": 36.0,
    },
}


METRIC_RULES = {
    "CPU Usage (%)": {
        "lower_is_better": True,
        "description": "CPU Usage shows the percentage of processor resources consumed while running the virtual machine workload. Lower CPU usage indicates better resource efficiency.",
    },
    "RAM Usage (GB)": {
        "lower_is_better": True,
        "description": "RAM Usage shows the amount of memory consumed by the virtual machine during testing. Lower RAM usage indicates better memory efficiency.",
    },
    "Disk Performance (MB/s)": {
        "lower_is_better": False,
        "description": "Disk Performance shows storage read/write throughput. Higher disk performance indicates faster storage operations.",
    },
    "Boot Time (seconds)": {
        "lower_is_better": True,
        "description": "Boot Time shows the time taken by the guest operating system to start. Lower boot time indicates faster startup performance.",
    },
}


def initialize_session_state():
    if "benchmark_data" not in st.session_state:
        st.session_state.benchmark_data = {
            platform: values.copy() for platform, values in DEFAULT_DATA.items()
        }


def rerun_app():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


def apply_dark_theme():
    st.markdown(
        """
        <style>
            .stApp {
                background: #0f172a;
                color: #e5e7eb;
            }

            [data-testid="stSidebar"] {
                background: #020617;
                border-right: 1px solid #1e293b;
            }

            [data-testid="stSidebar"] * {
                color: #e5e7eb;
            }

            .main-title {
                color: #f8fafc;
                font-size: 2.35rem;
                font-weight: 800;
                line-height: 1.2;
                margin-bottom: 0.35rem;
            }

            .subtitle {
                color: #94a3b8;
                font-size: 1.05rem;
                margin-bottom: 1.4rem;
            }

            .section-card {
                background: #111827;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 1.15rem;
                margin-bottom: 1rem;
                box-shadow: 0 12px 30px rgba(0, 0, 0, 0.18);
            }

            .section-card h3 {
                margin-top: 0;
                margin-bottom: 0.75rem;
            }

            .section-card p {
                margin-bottom: 0.5rem;
            }

            .section-card ul,
            .section-card ol {
                margin-top: 0.25rem;
                margin-bottom: 0;
                padding-left: 1.4rem;
            }

            .section-card li {
                margin-bottom: 0.35rem;
            }

            .metric-card {
                background: #111827;
                border: 1px solid #334155;
                border-left: 5px solid #38bdf8;
                border-radius: 10px;
                padding: 1rem;
                min-height: 118px;
                margin-bottom: 1rem;
            }

            .metric-label {
                color: #94a3b8;
                font-size: 0.9rem;
                font-weight: 650;
                margin-bottom: 0.45rem;
            }

            .metric-value {
                color: #f8fafc;
                font-size: 1.55rem;
                font-weight: 800;
            }

            .metric-note {
                color: #cbd5e1;
                font-size: 0.9rem;
                margin-top: 0.35rem;
            }

            .success-box {
                background: #052e1a;
                border: 1px solid #166534;
                border-left: 5px solid #22c55e;
                border-radius: 10px;
                padding: 1rem;
                color: #dcfce7;
                font-weight: 650;
                margin: 1rem 0;
            }

            .info-box {
                background: #082f49;
                border: 1px solid #0369a1;
                border-left: 5px solid #38bdf8;
                border-radius: 10px;
                padding: 1rem;
                color: #e0f2fe;
                margin: 1rem 0;
            }

            .workflow-box {
                background: #020617;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 1.2rem;
                text-align: center;
                color: #f8fafc;
                font-weight: 800;
                line-height: 2.1;
            }

            h1, h2, h3, h4 {
                color: #f8fafc;
            }

            p, li {
                color: #e5e7eb;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_benchmark_dataframe():
    dataframe = pd.DataFrame(st.session_state.benchmark_data).T
    dataframe.index.name = "Platform"
    return dataframe


def calculate_scores(dataframe):
    scores = {}

    for platform in dataframe.index:
        metric_scores = []

        for metric, rule in METRIC_RULES.items():
            value = float(dataframe.loc[platform, metric])

            if rule["lower_is_better"]:
                best_value = float(dataframe[metric].min())
                if value == 0:
                    score = 100 if best_value == 0 else 0
                else:
                    score = (best_value / value) * 100
            else:
                best_value = float(dataframe[metric].max())
                score = (value / best_value) * 100 if best_value != 0 else 0

            metric_scores.append(min(score, 100))

        scores[platform] = round(sum(metric_scores) / len(metric_scores), 2)

    return scores


def create_bar_chart(dataframe, selected_metric):
    figure, axis = plt.subplots(figsize=(8, 4.8))
    figure.patch.set_facecolor("#0f172a")
    axis.set_facecolor("#111827")

    bars = axis.bar(
        dataframe.index,
        dataframe[selected_metric],
        color=["#38bdf8", "#2dd4bf"],
        width=0.55,
    )

    axis.set_title(
        selected_metric + " Comparison",
        color="#f8fafc",
        fontsize=15,
        fontweight="bold",
        pad=16,
    )
    axis.set_ylabel(selected_metric, color="#e5e7eb", fontsize=11)
    axis.tick_params(colors="#e5e7eb", labelsize=10)
    axis.grid(axis="y", linestyle="--", alpha=0.22, color="#94a3b8")

    for spine in axis.spines.values():
        spine.set_color("#334155")

    for bar in bars:
        height = bar.get_height()
        axis.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            format(height, "g"),
            ha="center",
            va="bottom",
            color="#f8fafc",
            fontsize=11,
            fontweight="bold",
        )

    plt.tight_layout()
    return figure


def display_header():
    st.markdown(
        '<div class="main-title">Virtualization Performance Analyzer</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtitle">The Impact of Virtualization on System Performance: A Study of VMware vs VirtualBox</div>',
        unsafe_allow_html=True,
    )


def get_metric_winner(dataframe, metric):
    if METRIC_RULES[metric]["lower_is_better"]:
        return dataframe[metric].idxmin()
    return dataframe[metric].idxmax()


def get_overall_winner(scores):
    return max(scores, key=scores.get)


def get_score_difference(scores):
    return round(abs(scores["VMware"] - scores["VirtualBox"]), 2)


def create_card(title, body):
    clean_body = dedent(body).strip()

    st.markdown(
        f"""
<div class="section-card">
    <h3>{title}</h3>
    {clean_body}
</div>
        """,
        unsafe_allow_html=True,
    )


def create_kpi_card(label, value, note):
    st.markdown(
        f"""
<div class="metric-card">
    <div class="metric-label">{label}</div>
    <div class="metric-value">{value}</div>
    <div class="metric-note">{note}</div>
</div>
        """,
        unsafe_allow_html=True,
    )


def home_page():
    display_header()

    create_card(
        "Project Overview",
        """
        <p>
            This application analyzes the impact of virtualization on system
            performance by comparing VMware and VirtualBox. It provides an
            academic dashboard for entering benchmark values, visualizing
            performance differences, calculating scores, and generating a final
            recommendation.
        </p>
        """,
    )

    col1, col2 = st.columns(2)

    with col1:
        create_card(
            "Research Objectives",
            """
            <ul>
                <li>Compare VMware and VirtualBox using measurable performance metrics.</li>
                <li>Analyze CPU usage, RAM usage, disk performance, and boot time.</li>
                <li>Calculate a fair overall performance score.</li>
                <li>Generate a recommendation suitable for NTCC reporting.</li>
            </ul>
            """,
        )

    with col2:
        create_card(
            "Technology Stack",
            """
            <ul>
                <li>Python</li>
                <li>Streamlit</li>
                <li>Pandas</li>
                <li>Matplotlib</li>
            </ul>
            """,
        )

    create_card(
        "Application Features",
        """
        <ul>
            <li>Sidebar navigation with six academic project pages.</li>
            <li>User input page for custom benchmark values.</li>
            <li>Automatic performance score calculation.</li>
            <li>KPI cards, comparison charts, and metric descriptions.</li>
            <li>Final recommendation and report-ready conclusion.</li>
        </ul>
        """,
    )


def methodology_page():
    display_header()

    create_card(
        "Research Methodology",
        """
        <ol>
            <li>Configure VMware and VirtualBox with similar VM settings.</li>
            <li>Run the same benchmark workload on both platforms.</li>
            <li>Collect CPU, RAM, disk, and boot time values.</li>
            <li>Compare metrics using tables and graphs.</li>
            <li>Normalize values using score calculation formulas.</li>
            <li>Generate analysis and final recommendation.</li>
        </ol>
        """,
    )

    st.subheader("Workflow Diagram")
    st.markdown(
        """
<div class="workflow-box">
    VMware / VirtualBox<br>
    ↓<br>
    Benchmark Execution<br>
    ↓<br>
    Data Collection<br>
    ↓<br>
    Metric Comparison<br>
    ↓<br>
    Score Calculation<br>
    ↓<br>
    Result Analysis<br>
    ↓<br>
    Final Recommendation
</div>
        """,
        unsafe_allow_html=True,
    )

    create_card(
        "Research Significance",
        """
        <p>
            Virtualization is widely used in education, testing, cybersecurity
            labs, cloud computing, and enterprise infrastructure. This study
            helps identify how virtualization platforms affect resource usage
            and system performance.
        </p>
        """,
    )

    st.subheader("Performance Score Formula")
    st.latex(r"Score_{lower\ is\ better} = \frac{Best\ Lower\ Value}{Platform\ Value} \times 100")
    st.latex(r"Score_{higher\ is\ better} = \frac{Platform\ Value}{Best\ Higher\ Value} \times 100")
    st.latex(r"Overall\ Score = \frac{\sum Metric\ Scores}{Number\ of\ Metrics}")

    st.subheader("Benchmark Metrics")
    for metric, details in METRIC_RULES.items():
        rule_text = "Lower value is better." if details["lower_is_better"] else "Higher value is better."
        create_card(
            metric,
            f"""
            <p>{details["description"]}</p>
            <p><strong>Scoring Rule:</strong> {rule_text}</p>
            """,
        )


def input_page():
    display_header()

    st.markdown(
        """
<div class="info-box">
    Enter benchmark values for VMware and VirtualBox. Negative values are
    not allowed. The values update the dashboard automatically.
</div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Metric Explanation")
    exp1, exp2 = st.columns(2)

    with exp1:
        create_card("CPU Usage (%)", "<p>Processor consumption during VM workload execution. Lower is better.</p>")
        create_card("RAM Usage (GB)", "<p>Memory consumed by the virtual machine. Lower is better.</p>")

    with exp2:
        create_card("Disk Performance (MB/s)", "<p>Disk read/write throughput. Higher is better.</p>")
        create_card("Boot Time (seconds)", "<p>Time taken by the guest OS to start. Lower is better.</p>")

    vmware_col, virtualbox_col = st.columns(2)

    with vmware_col:
        st.subheader("VMware Input Values")

        st.session_state.benchmark_data["VMware"]["CPU Usage (%)"] = st.number_input(
            "VMware CPU Usage (%)",
            min_value=0.0,
            value=float(st.session_state.benchmark_data["VMware"]["CPU Usage (%)"]),
            step=1.0,
        )

        st.session_state.benchmark_data["VMware"]["RAM Usage (GB)"] = st.number_input(
            "VMware RAM Usage (GB)",
            min_value=0.0,
            value=float(st.session_state.benchmark_data["VMware"]["RAM Usage (GB)"]),
            step=0.1,
        )

        st.session_state.benchmark_data["VMware"]["Disk Performance (MB/s)"] = st.number_input(
            "VMware Disk Performance (MB/s)",
            min_value=0.0,
            value=float(st.session_state.benchmark_data["VMware"]["Disk Performance (MB/s)"]),
            step=5.0,
        )

        st.session_state.benchmark_data["VMware"]["Boot Time (seconds)"] = st.number_input(
            "VMware Boot Time (seconds)",
            min_value=0.0,
            value=float(st.session_state.benchmark_data["VMware"]["Boot Time (seconds)"]),
            step=1.0,
        )

    with virtualbox_col:
        st.subheader("VirtualBox Input Values")

        st.session_state.benchmark_data["VirtualBox"]["CPU Usage (%)"] = st.number_input(
            "VirtualBox CPU Usage (%)",
            min_value=0.0,
            value=float(st.session_state.benchmark_data["VirtualBox"]["CPU Usage (%)"]),
            step=1.0,
        )

        st.session_state.benchmark_data["VirtualBox"]["RAM Usage (GB)"] = st.number_input(
            "VirtualBox RAM Usage (GB)",
            min_value=0.0,
            value=float(st.session_state.benchmark_data["VirtualBox"]["RAM Usage (GB)"]),
            step=0.1,
        )

        st.session_state.benchmark_data["VirtualBox"]["Disk Performance (MB/s)"] = st.number_input(
            "VirtualBox Disk Performance (MB/s)",
            min_value=0.0,
            value=float(st.session_state.benchmark_data["VirtualBox"]["Disk Performance (MB/s)"]),
            step=5.0,
        )

        st.session_state.benchmark_data["VirtualBox"]["Boot Time (seconds)"] = st.number_input(
            "VirtualBox Boot Time (seconds)",
            min_value=0.0,
            value=float(st.session_state.benchmark_data["VirtualBox"]["Boot Time (seconds)"]),
            step=1.0,
        )

    if st.button("Reset to Default Values"):
        st.session_state.benchmark_data = {
            platform: values.copy() for platform, values in DEFAULT_DATA.items()
        }
        rerun_app()

    st.subheader("Current Benchmark Data")
    st.dataframe(get_benchmark_dataframe(), use_container_width=True)


def dashboard_page():
    display_header()

    dataframe = get_benchmark_dataframe()
    scores = calculate_scores(dataframe)
    overall_winner = get_overall_winner(scores)
    score_difference = get_score_difference(scores)

    st.subheader("Benchmark Data Table")
    st.dataframe(dataframe, use_container_width=True)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        create_kpi_card("VMware Score", str(scores["VMware"]) + "/100", "Overall normalized score")

    with kpi2:
        create_kpi_card("VirtualBox Score", str(scores["VirtualBox"]) + "/100", "Overall normalized score")

    with kpi3:
        create_kpi_card("Best Platform", overall_winner, "Highest overall score")

    with kpi4:
        create_kpi_card("Score Difference", str(score_difference), "Performance gap")

    st.subheader("Metric Comparison Chart")
    selected_metric = st.selectbox("Select Metric", list(METRIC_RULES.keys()))
    st.pyplot(create_bar_chart(dataframe, selected_metric))

    metric_winner = get_metric_winner(dataframe, selected_metric)
    rule_text = "Lower value is better." if METRIC_RULES[selected_metric]["lower_is_better"] else "Higher value is better."

    create_card(
        "Metric Description",
        f"""
        <p>{METRIC_RULES[selected_metric]["description"]}</p>
        <p><strong>Interpretation:</strong> {rule_text}</p>
        <p><strong>Better Platform for this metric:</strong> {metric_winner}</p>
        """,
    )


def results_page():
    display_header()

    dataframe = get_benchmark_dataframe()
    scores = calculate_scores(dataframe)
    winner = get_overall_winner(scores)
    score_difference = get_score_difference(scores)

    st.subheader("Overall Performance Scores")
    score_dataframe = pd.DataFrame(
        {
            "Platform": list(scores.keys()),
            "Overall Performance Score": list(scores.values()),
        }
    )
    st.dataframe(score_dataframe, use_container_width=True, hide_index=True)

    st.markdown(
        f"""
<div class="success-box">
    Final Recommendation: {winner} performs better overall based on the
    calculated benchmark score. The score difference is {score_difference:.2f} points.
</div>
        """,
        unsafe_allow_html=True,
    )

    vmware_cpu = dataframe.loc["VMware", "CPU Usage (%)"]
    virtualbox_cpu = dataframe.loc["VirtualBox", "CPU Usage (%)"]
    vmware_ram = dataframe.loc["VMware", "RAM Usage (GB)"]
    virtualbox_ram = dataframe.loc["VirtualBox", "RAM Usage (GB)"]
    vmware_disk = dataframe.loc["VMware", "Disk Performance (MB/s)"]
    virtualbox_disk = dataframe.loc["VirtualBox", "Disk Performance (MB/s)"]
    vmware_boot = dataframe.loc["VMware", "Boot Time (seconds)"]
    virtualbox_boot = dataframe.loc["VirtualBox", "Boot Time (seconds)"]

    cpu_winner = "VMware" if vmware_cpu <= virtualbox_cpu else "VirtualBox"
    ram_winner = "VMware" if vmware_ram <= virtualbox_ram else "VirtualBox"
    disk_winner = "VMware" if vmware_disk >= virtualbox_disk else "VirtualBox"
    boot_winner = "VMware" if vmware_boot <= virtualbox_boot else "VirtualBox"

    st.subheader("Detailed Academic Analysis")

    create_card(
        "CPU Comparison",
        f"""
        <p>
            VMware recorded CPU usage of <strong>{vmware_cpu:g}%</strong>, while VirtualBox
            recorded <strong>{virtualbox_cpu:g}%</strong>. Since lower CPU usage indicates better
            processor efficiency, <strong>{cpu_winner}</strong> performs better in CPU utilization.
        </p>
        """,
    )

    create_card(
        "RAM Comparison",
        f"""
        <p>
            VMware used <strong>{vmware_ram:g} GB</strong> of RAM, while VirtualBox used
            <strong>{virtualbox_ram:g} GB</strong>. Since lower RAM usage indicates better memory
            efficiency, <strong>{ram_winner}</strong> performs better in RAM management.
        </p>
        """,
    )

    create_card(
        "Disk Performance Comparison",
        f"""
        <p>
            VMware achieved disk performance of <strong>{vmware_disk:g} MB/s</strong>, while
            VirtualBox achieved <strong>{virtualbox_disk:g} MB/s</strong>. Since higher disk throughput
            is better, <strong>{disk_winner}</strong> performs better in disk operations.
        </p>
        """,
    )

    create_card(
        "Boot Time Comparison",
        f"""
        <p>
            VMware booted in <strong>{vmware_boot:g} seconds</strong>, while VirtualBox booted
            in <strong>{virtualbox_boot:g} seconds</strong>. Since lower boot time is better,
            <strong>{boot_winner}</strong> performs better in startup efficiency.
        </p>
        """,
    )

    create_card(
        "Final Recommendation",
        f"""
        <p>
            Based on normalized performance scoring, <strong>{winner}</strong> is recommended
            as the better virtualization platform for the tested benchmark conditions.
        </p>
        """,
    )

    create_card(
        "Conclusion",
        f"""
        <p>
            This NTCC project demonstrates that virtualization platforms can have
            a measurable impact on system performance. The comparison between VMware
            and VirtualBox shows differences in resource consumption, storage
            throughput, and startup time. Based on the current benchmark data,
            <strong>{winner}</strong> achieves the higher overall score.
        </p>
        <p>
            For final academic reporting, benchmark values should be collected from
            the same host system using identical virtual machine configurations and
            repeated test runs.
        </p>
        """,
    )


def about_page():
    display_header()

    create_card(
        "Project Title",
        "<p>The Impact of Virtualization on System Performance: A Study of VMware vs VirtualBox</p>",
    )

    col1, col2 = st.columns(2)

    with col1:
        create_card(
            "Team Members",
            """
            <ul>
                <li>Vaishnav Biju</li>
                <li>Payam Javaid Pandit</li>
                <li>Swastika Bansal</li>
            </ul>
            """,
        )

        create_card("Program", "<p>B.Tech CSE Semester V</p>")

    with col2:
        create_card(
            "Technologies Used",
            """
            <ul>
                <li>Python</li>
                <li>Streamlit</li>
                <li>Pandas</li>
                <li>Matplotlib</li>
            </ul>
            """,
        )

        create_card(
            "Project Purpose",
            """
            <p>
                The purpose of this project is to evaluate how virtualization affects
                system performance and compare VMware and VirtualBox using measurable
                benchmark metrics.
            </p>
            """,
        )

    create_card(
        "Future Scope",
        """
        <ul>
            <li>Cloud platform benchmarking</li>
            <li>Hyper-V comparison</li>
            <li>KVM comparison</li>
            <li>Real-time monitoring</li>
            <li>Automated benchmark execution</li>
        </ul>
        """,
    )


def main():
    st.set_page_config(
        page_title="Virtualization Performance Analyzer",
        page_icon="VPA",
        layout="wide",
    )

    initialize_session_state()
    apply_dark_theme()

    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio(
        "Select Page",
        [
            "Home",
            "Methodology",
            "Input Data",
            "Comparison Dashboard",
            "Results & Analysis",
            "About Project",
        ],
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("B.Tech NTCC Project")
    st.sidebar.caption("VMware vs VirtualBox")

    if selected_page == "Home":
        home_page()
    elif selected_page == "Methodology":
        methodology_page()
    elif selected_page == "Input Data":
        input_page()
    elif selected_page == "Comparison Dashboard":
        dashboard_page()
    elif selected_page == "Results & Analysis":
        results_page()
    elif selected_page == "About Project":
        about_page()


if __name__ == "__main__":
    main()