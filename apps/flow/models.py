from django.db import models

from apps.common.models import BaseModel

class FlowFile(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.name} ( {self.description} )'

class NodeClass(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    code = models.FileField(upload_to="node_classes")
    
    def __str__(self):
        return f'{self.name} ( {self.description} ) [Code: {self.code.name}]'
    
class Node(NodeClass):
    flow_file = models.ForeignKey(FlowFile, on_delete=models.CASCADE, related_name="nodes")

    def __str__(self):
        return f"{super().__str__()} [Flow: {self.flow_file}]"

class Parameter(BaseModel):
    name = models.CharField(max_length=100)
    node = models.ForeignKey(NodeClass, on_delete=models.CASCADE, related_name="parameters")
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.name} ( {self.description} )'

class Connections(BaseModel):
    source = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name="connection_source")
    target = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name="connection_target")
    
    def __str__(self):
        return f'{self.source.node.class_name} -> {self.target}'

