#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

struct Light {
    vec3 position;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

uniform Light light;
uniform sampler2D u_txt_0;
uniform vec3 camPos;

vec3 getLight(vec3 color) {
    vec3 Normal = normalize(normal);
    vec3 amb = light.ambient;

    vec3 light_dir = normalize(light.position - fragPos);
    float diff = max(0, dot(light_dir, Normal));
    vec3 vdif = diff * light.diffuse;

    // specular lighting calc
    vec3 view_dir = normalize(camPos - fragPos) ;
    vec3 reflect_dir = reflect(-light_dir, Normal);
    float spec = pow (max (dot (view_dir, reflect_dir), 0 ), 32);
    vec3 vspec = spec * light.specular;

    return color * (amb + vdif + vspec);
}

void main() {
    vec3 color = texture(u_txt_0, uv_0).rgb;
    color = getLight(color);
    fragColor = vec4(color, 1.0);
}