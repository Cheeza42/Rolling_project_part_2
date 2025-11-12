{{- /* 
Define a short app name. 
Used as a fallback when fullnameOverride isn't provided. 
Ensures the name is <=63 characters and doesn't end with '-'.
*/ -}}
{{- define "app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- /* 
Define the full release name (app.fullname). 
If fullnameOverride is set in values, it uses that.
Otherwise, combines the Helm release name and chart name safely.
*/ -}}
{{- define "app.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- /* 
Define common labels for all Kubernetes resources.
Includes the Helm release name and instance identifiers.
*/ -}}
{{- define "app.labels" -}}
app: {{ .Release.Name }}
app.kubernetes.io/name: {{ include "app.name" . | default .Release.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
