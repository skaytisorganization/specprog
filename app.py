from core import *
from spyre import server

#reading regions from reg2.txt
regions = []
with open("reg2.txt") as f:
	for l in f:
		(key, val) = l.split(':')
		regions.append({"label": val, "value": key })

class vhi_app(server.App):
	title = "VHI"

	inputs = [		{	"input_type":'dropdown',
                   		"label": 'Region', 
                    	"options" : regions,
                    	"variable_name": 'region', 
                    	"action_id": "update_data" },
                    {	"input_type":'dropdown',
                   		"label": 'Index  ', 
                    	"options" : [{"label": "VCI", "value": "VCI"},
                    			{"label": "TCI", "value": "TCI"},
                    			{"label": "VHI", "value": "VHI"}],
                    	"variable_name": 'index', 
                    	"action_id": "update_data" },
                    {   "input_type":"text",
                		"variable_name":"year",
                		"label": "Year",
                		"action_id": "update_data",
                		"value":1982  },
                    {   "input_type":"text",
                		"variable_name":"first",
                		"label": "First week",
                		"action_id": "update_data",
                		"value":1   }, 
                	{   "input_type":"text",
                		"variable_name":"second",
                		"label": "Second week",
                		"action_id": "update_data",
                		"value":1   }]

	tabs = ["Table", "Plot"]

	controls = [{   "control_type" : "button",
                    "label" : "Update",
                    "control_id" : "update_data"}]

	outputs = [{   "output_type" : "table",
                    "output_id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True },
                    {    "output_type" : "plot",
                    "output_id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot",  
                    "on_page_load" : False }]


	def getData(self, params):
		region = params['region']
		index = params['index']
		fst = params['first']
		sec = params['second']
		year = params['year']
		df = get_data_frame()
		return df[['Year','Week', index]][ (df['Region']==int(region)) & (df['Year']==int(year)) & (df['Week'] >= int(fst)) & (df['Week'] <= int(sec)) ]

	def getPlot(self, params):
		df = self.getData(params)
		plt_obj = df.plot(x='Week', y=params['index'])
		plt_obj.set_ylabel(params['index'])
		plt_obj.set_title(params['index'] + " plot")
		fig = plt_obj.get_figure()
		return fig

app = vhi_app()
app.launch(port=9093)
