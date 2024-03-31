




class Activity:
    def __init__(self, name, processes):
        """
            Activity: Represents an overall activity like vaccination or spraying. It takes a name and a list of processes.
        """
        self.name = name
        self.processes = processes

class Process:
    """
        Process: Represents a process within an activity. It has a name and a list of alerts.
    """
    def __init__(self, name, alerts):
        self.name = name
        self.alerts = alerts

class Alert:
    """
        Alert: Represents an alert or notification within a process. It has a name and a list of inputs.
    """
    def __init__(self, name, inputs):
        self.name = name
        self.inputs = inputs

class Input:
    def __init__(self, name, value):
        self.name = name
        self.value = value

# Example usage
vaccination_activity = Activity(
    "Vaccination",
    [
        Process(
            "Registration",
            [
                Alert(
                    "Collect Personal Details",
                    [
                        Input("Name", ""),
                        Input("Age", ""),
                        Input("Address", ""),
                    ]
                ),
                Alert(
                    "Collect Medical History",
                    [
                        Input("Allergies", ""),
                        Input("Previous Vaccinations", ""),
                    ]
                ),
            ]
        ),
        Process(
            "Vaccination Procedure",
            [
                Alert(
                    "Administer Vaccine",
                    [
                        Input("Vaccine Type", ""),
                        Input("Dose", ""),
                    ]
                ),
                Alert(
                    "Monitor for Side Effects",
                    [
                        Input("Temperature", ""),
                        Input("Other Symptoms", ""),
                    ]
                ),
            ]
        ),
        Process(
            "Follow-up",
            [
                Alert(
                    "Schedule Next Dose",
                    [
                        Input("Next Appointment Date", ""),
                    ]
                ),
            ]
        ),
    ]
)

# You can now access and modify the activity, processes, alerts, and inputs
# For example:
print(f"Activity: {vaccination_activity.name}")
for process in vaccination_activity.processes:
    print(f"  Process: {process.name}")
    for alert in process.alerts:
        print(f"    Alert: {alert.name}")
        for input_data in alert.inputs:
            print(f"      Input: {input_data.name} - {input_data.value}")