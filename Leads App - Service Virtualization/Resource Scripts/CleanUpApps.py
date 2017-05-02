from cloudshell.api.cloudshell_api import CloudShellAPISession, AttributeNameValue
from os import environ as parameter
import json

connectivity = json.loads(parameter["QUALICONNECTIVITYCONTEXT"])
reservationDetails = json.loads(parameter["RESERVATIONCONTEXT"])
resourceDetails = json.loads(parameter["RESOURCECONTEXT"])

domains_to_scan = parameter["domains"].split(',')
dry_run = parameter["dry_run"] != "False"


for domain in domains_to_scan:
    api = CloudShellAPISession(host=connectivity["serverAddress"], token_id=connectivity["adminAuthToken"], domain=domain)
    domain_details = api.GetDomainDetails(domain)
    resources_to_delete = [resource for resource in api.FindResources(resourceFamily='Deployed App', showAllDomains=domain == 'Global').Resources
                           if resource.FullPath is not None and hasattr(api.GetResourceDetails(resource.FullPath).VmDetails, 'UID')]
    resources_to_delete.extend([resource for resource in api.FindResources(resourceFamily='Generic App Family', showAllDomains=domain == 'Global').Resources
                                if resource.FullPath is not None and hasattr(api.GetResourceDetails(resource.FullPath).VmDetails, 'UID')])
    resources_to_delete.extend([resource for resource in api.FindResources(resourceFamily='Virtual Machine', showAllDomains=domain == 'Global').Resources
                                if resource.FullPath is not None and hasattr(api.GetResourceDetails(resource.FullPath).VmDetails, 'UID')])
    resources_to_delete.extend([resource for resource in api.FindResources(resourceFamily='Web Applications', showAllDomains=domain == 'Global').Resources
                                if resource.FullPath is not None and hasattr(api.GetResourceDetails(resource.FullPath).VmDetails, 'UID')])
    for resource in resources_to_delete:
        if not dry_run:
            api.DeleteResource(resource.FullPath)
        print("Deleted resource {}".format(resource.FullPath))

    api.Logoff()
