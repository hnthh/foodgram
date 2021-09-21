import re

from recipes.models import Recipe


class BaseService:
    def __init__(self, name, text, image, cooking_time, ingredients, tags):
        self.name = name
        self.text = text
        self.image = image
        self.cooking_time = cooking_time
        self.ingredients = ingredients
        self.tags = tags

    def set_recipe_ingredients(self, recipe):
        from recipes.models import RecipeIngredient

        ingredients = list()
        for item in self.ingredients:
            ingredient, amount = item.values()
            ingredients.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=amount,
                ),
            )

        RecipeIngredient.objects.bulk_create(ingredients)


class RecipeCreator(BaseService):
    def __init__(
        self,
        author,
        name,
        text,
        image,
        cooking_time,
        ingredients,
        tags,
    ):
        super().__init__(name, text, image, cooking_time, ingredients, tags)

        self.author = author

    def __call__(self):
        recipe = self.create()

        self.set_recipe_ingredients(recipe)
        recipe.tags.set(self.tags)

        return recipe

    def create(self):
        return Recipe.objects.create(
            author=self.author,
            name=self.name,
            text=self.text,
            image=self.image,
            cooking_time=self.cooking_time,
        )


class RecipeUpdater(BaseService):
    def __init__(
        self,
        recipe,
        name=None,
        text=None,
        image=None,
        cooking_time=None,
        ingredients=None,
        tags=None,
    ):
        super().__init__(name, text, image, cooking_time, ingredients, tags)

        self.recipe = recipe
        self.nested = ('ingredients', 'tags')

    def __call__(self):
        recipe = self.update()
        recipe.save()

        return recipe

    def update(self):
        update = [
            attrib for attrib in dir(self)
            if re.match('^[a-zA-Z]+.*', attrib)
            and attrib not in ('recipe', 'nested', 'update')
            and getattr(self, attrib) is not None
        ]

        if 'tags' in update:
            self.recipe.tags.remove()
            self.recipe.tags.set(self.tags)

        if 'ingredients' in update:
            self.recipe.recipeingredients.all().delete()
            self.set_recipe_ingredients(self.recipe)

        for attr in update:
            if attr not in self.nested:
                value = getattr(self, attr)
                setattr(self.recipe, attr, value)

        return self.recipe
