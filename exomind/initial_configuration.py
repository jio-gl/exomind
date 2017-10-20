
initial_exomind = '''
<exomind_configuration>
    <path>.</path>
    <database_user>root</database_user>
    <database_password></database_password>
    <http_proxy></http_proxy>
    <https_proxy></https_proxy>
    <focus_region_size>50</focus_region_size>
    <sleep_secs_on_failure>120</sleep_secs_on_failure>
    <crawl_batch_size>1</crawl_batch_size>
    <ps_viewer>evince</ps_viewer>
</exomind_configuration>
'''

initial_bots = '''
<bots>

  <bot>
    <class>YouTubeBot</class>
    <user></user>
    <pass></pass>
    <sleep_regular_secs>5.0</sleep_regular_secs>
    <sleep_random_bool>1</sleep_random_bool>
    <sleep_module_gets>1</sleep_module_gets>
    <chatbot>0</chatbot>
    </bot>

  <bot>
    <class>FlickrBot</class>
    <user></user>
    <pass></pass>
    <sleep_regular_secs>5.0</sleep_regular_secs>
    <sleep_random_bool>1</sleep_random_bool>
    <sleep_module_gets>1</sleep_module_gets>
    <chatbot>0</chatbot>
    </bot>


<bot>
    <class>TwitterBot</class>
    <user></user>
    <pass></pass> 
    <sleep_regular_secs>5.0</sleep_regular_secs>
    <sleep_random_bool>1</sleep_random_bool>
    <sleep_module_gets>1</sleep_module_gets>
    <chatbot>0</chatbot>
    </bot>

<bot>
    <class>SearchEngineBot</class>
    <user></user>
    <pass></pass>
    <sleep_regular_secs>5.0</sleep_regular_secs>
    <sleep_random_bool>1</sleep_random_bool>
    <sleep_module_gets>1</sleep_module_gets>
    <chatbot>0</chatbot>
    </bot>

<bot>
    <class>FacebookBot</class>
    <user></user>
    <pass></pass>
    <sleep_regular_secs>5.0</sleep_regular_secs>
    <sleep_random_bool>1</sleep_random_bool>
    <sleep_module_gets>1</sleep_module_gets>
    <chatbot>0</chatbot>
    </bot>

<bot>
    <class>LinkedInBot</class>
    <user></user>
    <pass></pass>
    <sleep_regular_secs>5.0</sleep_regular_secs>
    <sleep_random_bool>1</sleep_random_bool>
    <sleep_module_gets>1</sleep_module_gets>
    <chatbot>0</chatbot>
    </bot>

<bot>
    <class>GraphBot</class>
    <user></user>
    <pass></pass>
    <sleep_regular_secs>5.0</sleep_regular_secs>
    <sleep_random_bool>1</sleep_random_bool>
    <sleep_module_gets>1</sleep_module_gets>
    <chatbot>0</chatbot>
    </bot>

<bot>
    <class>MSNBot</class>
    <user></user>
    <pass></pass>
    <sleep_regular_secs>5.0</sleep_regular_secs>
    <sleep_random_bool>1</sleep_random_bool>
    <sleep_module_gets>1</sleep_module_gets>
    <chatbot>1</chatbot>
    </bot>

<bot>
    <class>GtalkBot</class>
    <user></user>
    <pass></pass>
    <sleep_regular_secs>5.0</sleep_regular_secs>
    <sleep_random_bool>1</sleep_random_bool>
    <sleep_module_gets>1</sleep_module_gets>
    <chatbot>1</chatbot>
    </bot>

</bots>
'''

initial_expanders = '''
<expanders>

  <expander>
    <class>YouTubeBot</class>
    <method>users_from_favorite_videos</method>
    </expander>

  <expander>
    <class>FlickrBot</class>
    <method>users_from_favorite_photos</method>
    </expander>

  <expander>  
    <class>SearchEngineBot</class>
    <method>name_to_emails</method>
    </expander>

  <expander>  
    <class>SearchEngineBot</class>
    <method>name_to_emails_strong</method>
    </expander>

  <expander>  
    <class>SearchEngineBot</class>
    <method>domain_to_emails</method>
    </expander>

  <expander>  
    <class>SearchEngineBot</class>
    <method>domain_to_emails_strong</method>
    </expander>

  <expander>  
    <class>SearchEngineBot</class>
    <method>name_to_self_emails</method>
    </expander>

  <expander>  
    <class>SearchEngineBot</class>
    <method>vocabulary</method>
    </expander>

  <expander>  
    <class>GraphBot</class>
    <method>neighbors</method>
    </expander>

  <expander>  
    <class>GraphBot</class>
    <method>with_all</method>
    </expander>

</expanders>
'''

initial_weigh_scales = '''
<weigh_scales>

  <weigh_scale>  
    <class>SearchEngineBot</class>
    <method>normalized_se_entropy</method>
    <min_weight>0.0</min_weight>
    <max_weight>0.5</max_weight>
    <context></context>
    </weigh_scale>

  <weigh_scale>  
    <class>SearchEngineBot</class>
    <method>se_hits</method>
    <min_weight>1</min_weight>
    <max_weight>10000</max_weight>
    <context></context>
    </weigh_scale>

  <weigh_scale>  
    <class>SearchEngineBot</class>
    <method>normalized_se_distance</method>
    <min_weight>0.0</min_weight>
    <max_weight>0.5</max_weight>
    <context></context>
    </weigh_scale>

  <weigh_scale>  
    <class>SearchEngineBot</class>
    <method>jaccard_distance</method>
    <min_weight>-2.0</min_weight>
    <max_weight>2.0</max_weight>
    <context></context>
    </weigh_scale>

  <weigh_scale>  
    <class>SearchEngineBot</class>
    <method>hits_distance</method>
    <min_weight>0</min_weight>
    <max_weight>100000</max_weight>
    <context></context>
    </weigh_scale>

  <weigh_scale>  
    <class>GraphBot</class>
    <method>ofuscate</method>
    <min_weight>0.0</min_weight>
    <max_weight>0.0</max_weight>
    <context></context>
    </weigh_scale>

</weigh_scales>
'''