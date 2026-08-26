from collections import Counter


def _get_data(document):
    """
    Extract architecture JSON from a Chroma document.
    """

    import json

    content = document.page_content

    marker = "Architecture Data:\n"

    if marker not in content:
        return {}

    json_data = content.split(marker, 1)[1]

    try:
        return json.loads(json_data)
    except json.JSONDecodeError:
        return {}


def _get_project(data):
    project = data.get("project", {})

    if isinstance(project, dict):
        return project

    return {}


def _get_stack(data):
    stack = data.get("recommended_stack", {})

    if isinstance(stack, dict):
        return stack

    return {}


def _extract_components(data):
    """
    Extract technologies from recommended_stack.
    """

    stack = _get_stack(data)

    components = set()

    for value in stack.values():

        if isinstance(value, str):
            components.add(value)

    return components


def _extract_patterns(data):
    """
    Extract architecture pattern.
    """

    project = _get_project(data)

    pattern = project.get("arch")

    if isinstance(pattern, str):
        return {pattern}

    return set()


def _extract_cloud(data):
    """
    Extract cloud/deployment provider.
    """

    project = _get_project(data)

    cloud = project.get("cloud")

    if isinstance(cloud, str):
        return cloud

    return None


def _extract_type(data):
    """
    Extract architecture type.
    """

    project = _get_project(data)

    architecture_type = project.get("type")

    if isinstance(architecture_type, str):
        return architecture_type

    return None


def _extract_scale(data):
    """
    Extract important scale metrics.
    """

    project = _get_project(data)

    scale = {}

    numeric_fields = [
        "dau",
        "concurrent",
        "transactions_per_day",
        "daily_transactions",
        "daily_requests",
        "requests_per_day",
        "live_streams",
        "vod_uploads",
        "daily_streams",
        "fraud_alerts",
        "active_accounts",
        "loan_applications",
        "certificates_issued",
        "courses_catalog_size",
    ]

    for field in numeric_fields:

        value = project.get(field)

        if isinstance(value, (int, float)):
            scale[field] = value

    return scale


def _extract_sla(data):
    project = _get_project(data)

    return project.get("sla")


def _extract_geo(data):
    project = _get_project(data)

    return project.get("geo")


def _extract_budget(data):
    project = _get_project(data)

    return project.get("budget")


def _extract_compliance(data):
    project = _get_project(data)

    return project.get("compliance")


def _extract_reasoning(data):
    """
    Extract expert reasoning stored with the architecture.
    """

    reasoning = data.get("reasoning", [])

    if isinstance(reasoning, list):
        return [
            item
            for item in reasoning
            if isinstance(item, str)
        ]

    return []


def analyze_architecture_set(documents):

    component_counter = Counter()
    pattern_counter = Counter()
    cloud_counter = Counter()
    type_counter = Counter()
    geo_counter = Counter()
    budget_counter = Counter()
    compliance_counter = Counter()

    reasoning_points = []

    scale_values = {}

    architecture_count = len(documents)

    for document in documents:

        data = _get_data(document)

        if not data:
            continue

        # ----------------------------------------------
        # Technologies
        # ----------------------------------------------

        components = _extract_components(data)

        for component in components:
            component_counter[component] += 1

        # ----------------------------------------------
        # Architecture patterns
        # ----------------------------------------------

        patterns = _extract_patterns(data)

        for pattern in patterns:
            pattern_counter[pattern] += 1

        # ----------------------------------------------
        # Cloud
        # ----------------------------------------------

        cloud = _extract_cloud(data)

        if cloud:
            cloud_counter[cloud] += 1

        # ----------------------------------------------
        # Type
        # ----------------------------------------------

        architecture_type = _extract_type(data)

        if architecture_type:
            type_counter[architecture_type] += 1

        # ----------------------------------------------
        # Geography
        # ----------------------------------------------

        geo = _extract_geo(data)

        if geo:
            geo_counter[geo] += 1

        # ----------------------------------------------
        # Budget
        # ----------------------------------------------

        budget = _extract_budget(data)

        if budget:
            budget_counter[budget] += 1

        # ----------------------------------------------
        # Compliance
        # ----------------------------------------------

        compliance = _extract_compliance(data)

        if compliance:
            compliance_counter[compliance] += 1

        # ----------------------------------------------
        # Scale
        # ----------------------------------------------

        scale = _extract_scale(data)

        for field, value in scale.items():

            if field not in scale_values:
                scale_values[field] = []

            scale_values[field].append(value)

        # ----------------------------------------------
        # Expert reasoning
        # ----------------------------------------------

        reasoning = _extract_reasoning(data)

        reasoning_points.extend(reasoning)

    return {
        "architecture_count": architecture_count,

        "components": component_counter,

        "patterns": pattern_counter,

        "clouds": cloud_counter,

        "types": type_counter,

        "geo": geo_counter,

        "budget": budget_counter,

        "compliance": compliance_counter,

        "scale": scale_values,

        "reasoning": reasoning_points,
    }


def _format_scale(scale_values):

    lines = []

    for field, values in scale_values.items():

        if not values:
            continue

        minimum = min(values)
        maximum = max(values)
        average = sum(values) / len(values)

        lines.append(
            f"- {field}: "
            f"min={minimum:,}, "
            f"max={maximum:,}, "
            f"average={average:,.0f}"
        )

    return lines


def build_intelligence_context(
    intelligence,
    top_components=10,
    top_patterns=10,
    top_clouds=5,
    top_types=10,
    top_reasoning=10,
):

    architecture_count = intelligence[
        "architecture_count"
    ]

    lines = []

    lines.append(
        f"Analysis based on {architecture_count} "
        f"similar Kernx architectures."
    )

    # ==================================================
    # TECHNOLOGIES
    # ==================================================

    lines.append("\nCOMMON TECHNOLOGIES:")

    for component, count in intelligence[
        "components"
    ].most_common(top_components):

        percentage = (
            count / architecture_count * 100
            if architecture_count
            else 0
        )

        lines.append(
            f"- {component}: "
            f"{count}/{architecture_count} "
            f"({percentage:.0f}%)"
        )

    # ==================================================
    # ARCHITECTURE PATTERNS
    # ==================================================

    lines.append("\nARCHITECTURE PATTERNS:")

    for pattern, count in intelligence[
        "patterns"
    ].most_common(top_patterns):

        percentage = (
            count / architecture_count * 100
            if architecture_count
            else 0
        )

        lines.append(
            f"- {pattern}: "
            f"{count}/{architecture_count} "
            f"({percentage:.0f}%)"
        )

    # ==================================================
    # CLOUD
    # ==================================================

    lines.append("\nCLOUD / DEPLOYMENT:")

    for cloud, count in intelligence[
        "clouds"
    ].most_common(top_clouds):

        percentage = (
            count / architecture_count * 100
            if architecture_count
            else 0
        )

        lines.append(
            f"- {cloud}: "
            f"{count}/{architecture_count} "
            f"({percentage:.0f}%)"
        )

    # ==================================================
    # ARCHITECTURE TYPES
    # ==================================================

    lines.append("\nARCHITECTURE TYPES:")

    for architecture_type, count in intelligence[
        "types"
    ].most_common(top_types):

        percentage = (
            count / architecture_count * 100
            if architecture_count
            else 0
        )

        lines.append(
            f"- {architecture_type}: "
            f"{count}/{architecture_count} "
            f"({percentage:.0f}%)"
        )

    # ==================================================
    # GEOGRAPHY
    # ==================================================

    lines.append("\nGEOGRAPHY:")

    for geo, count in intelligence[
        "geo"
    ].most_common():

        percentage = (
            count / architecture_count * 100
            if architecture_count
            else 0
        )

        lines.append(
            f"- {geo}: "
            f"{count}/{architecture_count} "
            f"({percentage:.0f}%)"
        )

    # ==================================================
    # BUDGET
    # ==================================================

    lines.append("\nBUDGET TIERS:")

    for budget, count in intelligence[
        "budget"
    ].most_common():

        percentage = (
            count / architecture_count * 100
            if architecture_count
            else 0
        )

        lines.append(
            f"- {budget}: "
            f"{count}/{architecture_count} "
            f"({percentage:.0f}%)"
        )

    # ==================================================
    # SCALE
    # ==================================================

    lines.append("\nSCALE RANGES:")

    lines.extend(
        _format_scale(
            intelligence["scale"]
        )
    )

    # ==================================================
    # EXPERT REASONING
    # ==================================================

    lines.append("\nEXPERT REASONING FROM KERNX:")

    seen = set()

    reasoning_count = 0

    for reasoning in intelligence["reasoning"]:

        if reasoning in seen:
            continue

        seen.add(reasoning)

        lines.append(
            f"- {reasoning}"
        )

        reasoning_count += 1

        if reasoning_count >= top_reasoning:
            break

    return "\n".join(lines)

def extract_current_stack(data):
    """
    Extract the technology stack from the user's architecture.
    """

    stack = data.get("recommended_stack", {})

    if not isinstance(stack, dict):
        return set()

    return {
        value
        for value in stack.values()
        if isinstance(value, str)
    }


def find_architecture_gaps(current_data, intelligence):
    """
    Compare the user's architecture against
    technologies commonly found in similar architectures.
    """

    current_components = extract_current_stack(
        current_data
    )

    common_components = intelligence["components"]

    missing_components = []

    architecture_count = intelligence[
        "architecture_count"
    ]

    for component, count in common_components.most_common():

        if component in current_components:
            continue

        percentage = (
            count / architecture_count * 100
            if architecture_count
            else 0
        )

        # Only consider components appearing
        # in at least 40% of similar architectures.
        if percentage >= 40:

            missing_components.append({
                "component": component,
                "count": count,
                "percentage": round(percentage),
            })

    return missing_components

def build_gap_context(
    missing_components,
    max_results=10,
):
    """
    Convert architecture gaps into LLM-friendly context.
    """

    if not missing_components:
        return (
            "No major technology gaps were detected "
            "against the retrieved Kernx architectures."
        )

    lines = [
        "POTENTIAL ARCHITECTURE GAPS:"
    ]

    for item in missing_components[:max_results]:

        lines.append(
            f"- {item['component']}: "
            f"used in {item['percentage']}% "
            f"of similar architectures"
        )

    return "\n".join(lines)