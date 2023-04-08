from xml.etree import ElementTree
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.Adapters import McPATAdapter
from MultiExplorer.src.config import PATH_RUNDIR

LINE_FILL = "------------------------------------------------------------------------"


def get_system(file_rundir_rel_path):
    absolute_file_path = PATH_RUNDIR + "/" + file_rundir_rel_path

    xml = ElementTree.parse(absolute_file_path)

    system_component = xml.getroot().find("component[@id='system']")

    return system_component


def compare_params(component_g, component_e):
    params = component_g.findall("param")

    param_diffs = 0

    for param in params:
        name = param.get('name')

        value = param.get('value')

        e_param = component_e.find("param[@name='" + name + "']")

        if e_param is None:
            print name + " param example not found"

            continue

        e_value = e_param.get('value')

        if value != e_value:
            param_diffs += 1

            print name + ": " + value + ' != ' + e_value

    return param_diffs


def compare_components(system_g, system_e):
    components = system_g.findall("component")

    for component in components:
        component_id = component.get("id")

        print component_id

        component_e = system_e.find("component[@id='" + component_id + "']")

        if component_e is None:
            print component_id + " component example not found"

            continue

        param_diffs = compare_params(component, component_e)

        if param_diffs == 0:
            print "no param differences between the components"

        compare_components(component, component_e)

    print LINE_FILL


mcpat_adapter = McPATAdapter()

mcpat_adapter.prepare()

g_system = get_system("mcpat_input.xml")

e_system = get_system("SniperSimArmA57Cholesky20220720_084449/SniperSimArmA57Cholesky_mcpatInput.xml")

# print "system"
#
# system_param_diffs = compare_params(g_system, e_system)
#
# if system_param_diffs == 0:
#     print "no system param differences found"
#
# print LINE_FILL
#
# compare_components(g_system, e_system)

compare_params(e_system, g_system)

compare_components(e_system, g_system)
