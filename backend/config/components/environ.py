from environ import Env, Path

root = Path(__file__) - 3
env = Env(
    DEBUG=(bool, False),
)

Env.read_env(
    root('../infra/.env'),
)

__all__ = [
    env,
]
